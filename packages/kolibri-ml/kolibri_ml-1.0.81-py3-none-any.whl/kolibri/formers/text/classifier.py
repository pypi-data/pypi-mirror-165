
from  kdmt.jupyter import isnotebook
from kolibri.config import ModelConfig
from kolibri.model_loader import ModelLoader
from kolibri.model_trainer import ModelTrainer
from kolibri.stopwords import get_stop_words
import os

import pandas as pd

from kolibri.logger import get_logger
import ipywidgets as ipw
from IPython.display import display, clear_output

logger=get_logger(__name__)


class TextClassiFormer():
    """
    Text classification pipeline

    """

    defaults={
        'track-experiments': False,
        'experiment-name':'experiment_1',
        'language': 'en',
        'do-lower-case':True,
        "evaluate-performance": True,
        "model": 'LogisticRegression',
        "remove-stopwords": True,
        "model_name": "classifier_file"
    }
    def __init__(self,output_folder, data, content, target, configs={}):

        for key in configs:
            if key not in self.defaults:
                self.defaults[key]=configs[key]

        self.verbose=isnotebook()
        progress=None
        if data is not None:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("data parameter should be a pandas Dataframe")
            if target not in list(data.columns):
                raise ValueError("target: "+ target+" not in the provided Dataframe")
            self.target=target
            self.content=content

            logger.info("Preparing display monitor")

            if self.verbose:
                progress = ipw.IntProgress(
                    value=0, min=0, max=4, step=1, description="Initialuzing: "
                )

                clear_output()
                display(progress)

            self.data=data
            self.defaults.update(configs)

            self.trainer=self._build(output_folder, progress)
            if self.verbose:
                clear_output()
                progress.value+=1
                progress.description="Saving Model"
                display(progress)
            model_directory = self.trainer.persist(output_folder, fixed_model_name=self.defaults["model_name"])
            if self.verbose:
                clear_output()
                progress.value+=1
                progress.description="Loading Model"
                display(progress)
            self.model_interpreter = ModelLoader.load(os.path.join(output_folder, self.defaults["model_name"]))
            if self.verbose:
                clear_output()
                progress.value+=1
                progress.description="Finished"
                display(progress)

    def __call__(self, data, target=None):

        res= self.model_interpreter.predict(data)

        res=pd.DataFrame(res).fillna(0)
        return res

    def _build(self, output_folder, progress=None):
        config = {}

        config['track-experiments'] = self.defaults['track-experiments']
        config['experiment-name'] = self.defaults['experiment-name']
        config['language'] = self.defaults['language']
        config['do-lower-case'] = self.defaults['do-lower-case']
        config["model"] = self.defaults["model"]
        config["evaluate-performance"] = self.defaults["evaluate-performance"]
        config['output-folder'] = output_folder
        config['pipeline'] = ['WordTokenizer', 'CollocationAnalyzer','TFIDFFeaturizer', 'SklearnEstimator']

        config["remove-stopwords"] = self.defaults["remove-stopwords"]
        for key in self.defaults:
            if key not in config:
                config[key]=self.defaults[key]

        trainer = ModelTrainer(ModelConfig(config))

        if progress and self.verbose:
            progress.value += 1
            progress.description = "Fitting model"
            clear_output()
            display(progress)
        self._data_x_train, self._data_y_train,self._data_x_test, self._data_y_test=self.preprocessing_pipeline=trainer.fit_transformers([v for v in self.data[self.content].values if v is not None], [v for v in self.data[self.target].values if v is not None])

        self._model=trainer.fit_estimator(self._data_x_train, self._data_y_train,self._data_x_test)

        return trainer


    def plot(self, plot="frequency", topic_num=None, save=False, system=True, display_format=None):

        """
        This function takes a trained model_type object (optional) and returns a plot based
        on the inferred dataset by internally calling assign_model before generating a
        plot. Where a model_type parameter is not passed, a plot on the entire dataset will
        be returned instead of one at the topic level. As such, plot_model can be used
        with or without model_type. All plots with a model_type parameter passed as a trained
        model_type object will return a plot based on the first topic i.e.  'Topic 0'. This
        can be changed using the topic_num param.



        model_type: object, default = none
            Trained Model Object


        plot: str, default = 'frequency'
            List of available plots (ID - Name):

            * Word Token Frequency - 'frequency'
            * Word Distribution Plot - 'distribution'
            * Bigram Frequency Plot - 'bigram'
            * Trigram Frequency Plot - 'trigram'
            * Sentiment Polarity Plot - 'sentiment'
            * Part of Speech Frequency - 'pos'
            * t-SNE (3d) Dimension Plot - 'tsne'
            * Topic Model (pyLDAvis) - 'topic_model'
            * Topic Infer Distribution - 'topic_distribution'
            * Wordcloud - 'wordcloud'
            * UMAP Dimensionality Plot - 'umap'


        topic_num : str, default = None
            Topic number to be passed as a string. If set to None, default generation will
            be on 'Topic 0'


        save: string/bool, default = False
            Plot is saved as png file in local directory when save parameter set to True.
            Plot is saved as png file in the specified directory when the path to the directory is specified.


        system: bool, default = True
            Must remain True all times. Only to be changed by internal functions.


        display_format: str, default = None
            To display plots in Streamlit (https://www.streamlit.io/), set this to 'streamlit'.
            Currently, not all plots are supported.


        Returns:
            None


        Warnings
        --------
        -  'pos' and 'umap' plot not available at model_type level. Hence the model_type parameter is
           ignored. The result will always be based on the entire training corpus.

        -  'topic_model' plot is based on pyLDAVis implementation. Hence its not available
           for model_type = 'lsi', 'rp' and 'nmf'.
        """
        if topic_num != None:
            topic_num="Topic_" + str(topic_num)
        from IPython.display import display, HTML, clear_output, update_display
        # setting default of topic_num
        if self._model is not None and topic_num is None:
            topic_num = "Topic 0"
            logger.info("Topic selected. topic_num : " + str(topic_num))

        import sys

        # plot checking
        allowed_plots = [
            "frequency",
            "bigram",
            "trigram",
#            "sentiment",
            "tsne",
            "topic_model",
            "topic_distribution",
            "wordcloud",

        ]
        if plot not in allowed_plots:
            sys.exit(
                "(Value Error): Plot Not Available. Please see docstring for list of available plots."
            )

        # handle topic_model plot error
        if plot == "topic_model":
            not_allowed_tm = ["lsi", "rp", "nmf"]
            if self.model_type in not_allowed_tm:
                sys.exit(
                    "(Type Error): Model not supported for plot = topic_model. Please see docstring for list of available models supported for topic_model."
                )

        # checking display_format parameter
        plot_formats = [None, "streamlit"]

        if display_format not in plot_formats:
            raise ValueError("display_format can only be None or 'streamlit'.")

        if display_format == "streamlit":
            try:
                import streamlit as st
            except ImportError:
                raise ImportError(
                    "It appears that streamlit is not installed. Do: pip install streamlit"
                )

        """
        error handling ends here
        """

        logger.info("Importing libraries")
        # import dependencies
        import pandas as pd

        # import cufflinks -->binds plotly to pandas
        import cufflinks as cf

        cf.go_offline()
        cf.set_config_file(offline=False, world_readable=True)

        # save parameter

        if save:
            save_param = True
        else:
            save_param = False

        logger.info("save_param set to " + str(save_param))

        logger.info("plot type: " + str(plot))

        if plot == "frequency":

            try:

                from sklearn.feature_extraction.text import CountVectorizer



                def get_top_n_words(corpus, n=None):
                    corpus = self.model_interpreter.pipeline.transformers[-1].transform(corpus)
                    corpus=[" ".join(c) for c in corpus]
                    vec = CountVectorizer()
                    logger.info("Fitting CountVectorizer()")
                    bag_of_words = vec.fit_transform(corpus)
                    sum_words = bag_of_words.sum(axis=0)
                    words_freq = [
                        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
                    ]
                    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
                    return words_freq[:n]

                logger.info("Rendering Visual")

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    common_words=[(w, c) for w, c in self._model.indexer.token2count.items()][:100]
#                    common_words = get_top_n_words([str(v) for v in self.data[self.target].values if v is not None], n=100)
                    df2 = pd.DataFrame(common_words, columns=["Text", "count"])

                    if display_format == "streamlit":
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 words after removing stop words",
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 words after removing stop words",
                                asFigure=save_param,
                            )
                        )

                else:
                    title = (
                            str(topic_num) + ": " + "Top 100 words after removing stop words"
                    )
                    logger.info(
                        "SubProcess predict() called =================================="
                    )
                    assigned_df = self( [v for v in self.data[self.target].values if v is not None])
                    logger.info(
                        "SubProcess () end =================================="
                    )
                    assigned_df[self.target]=self.data[self.target]
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]

#                    common_words=[(w, c) for w, c in self._model.indexer.token2count.items()][:100]
                    common_words = get_top_n_words([str(v) for v in filtered_df[self.target].values if v is not None], n=100)
                    df2 = pd.DataFrame(common_words, columns=["Text", "count"])

                    if display_format == "streamlit":
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=save_param,
                            )
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(self.defaults["output-folder"], "Word Frequency.html")
                    else:
                        plot_filename = "Word Frequency.html"
                    logger.info(f"Saving '{plot_filename}'")
                    df3.write_html(plot_filename)



            except Exception as e:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "bigram":

            try:

                from sklearn.feature_extraction.text import CountVectorizer

                def get_top_n_bigram(corpus, n=None):
                    logger.info("Fitting CountVectorizer()")
                    vec = CountVectorizer(ngram_range=(2, 2)).fit(corpus)
                    bag_of_words = vec.transform(corpus)
                    sum_words = bag_of_words.sum(axis=0)
                    words_freq = [
                        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
                    ]
                    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
                    return words_freq[:n]

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    common_words = get_top_n_bigram([v for v in self.data[self.target].values if v is not None], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 bigrams after removing stop words",
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 bigrams after removing stop words",
                                asFigure=save_param
                            )
                        )

                else:
                    title = (
                            str(topic_num) + ": " + "Top 100 bigrams after removing stop words"
                    )
                    logger.info(
                        "SubProcess predict() called =================================="
                    )
                    assigned_df = self([v for v in self.data[self.target].values if v is not None])
                    assigned_df[self.target]=self.data[self.target]

                    logger.info(
                        "SubProcess predict() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    common_words = get_top_n_bigram(filtered_df[self.target], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=save_param
                            )
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Bigram.html")
                    else:
                        plot_filename = "Bigram.html"
                    logger.info(f"Saving '{plot_filename}'")
                    df3.write_html(plot_filename)


            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "trigram":

            try:

                from sklearn.feature_extraction.text import CountVectorizer

                def get_top_n_trigram(corpus, n=None):
                    vec = CountVectorizer(ngram_range=(3, 3)).fit(corpus)
                    logger.info("Fitting CountVectorizer()")
                    bag_of_words = vec.transform(corpus)
                    sum_words = bag_of_words.sum(axis=0)
                    words_freq = [
                        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
                    ]
                    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
                    return words_freq[:n]

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    common_words = get_top_n_trigram([v for v in self.data[self.target].values if v is not None], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 trigrams after removing stop words",
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 trigrams after removing stop words",
                                asFigure=save_param
                            )
                        )

                else:
                    title = (
                            str(topic_num) + ": " + "Top 100 trigrams after removing stop words"
                    )
                    logger.info(
                        "SubProcess predict() called =================================="
                    )
                    assigned_df = self([v for v in self.data[self.target].values if v is not None])
                    assigned_df[self.target]=self.data[self.target]

                    logger.info(
                        "SubProcess predict() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    common_words = get_top_n_trigram(filtered_df[self.target], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=save_param
                            )
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Trigram.html")
                    else:
                        plot_filename = "Trigram.html"
                    logger.info(f"Saving '{plot_filename}'")
                    df3.write_html(plot_filename)

            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "sentiment":
            raise NotImplementedError

        elif plot == "tsne":

            logger.info(
                "SubProcess predict() called =================================="
            )
            b = self.model_interpreter.predict([v for v in self.data[self.target].values if v is not None], verbose=False)
            logger.info("SubProcess predict() end ==================================")
            b.dropna(axis=0, inplace=True)  # droping rows where Dominant_Topic is blank

            c = []
            for i in b.columns:
                if "Topic_" in i:
                    a = i
                    c.append(a)

            bb = b[c]

            from sklearn.manifold import TSNE

            logger.info("Fitting TSNE()")
            X_embedded = TSNE(n_components=3).fit_transform(bb)

            logger.info("Sorting Dataframe")
            X = pd.DataFrame(X_embedded)
            X["Dominant_Topic"] = b["Dominant_Topic"]
            X.sort_values(by="Dominant_Topic", inplace=True)
            X.dropna(inplace=True)

            logger.info("Rendering Visual")
            import plotly.express as px

            df = X
            fig = px.scatter_3d(
                df,
                x=0,
                y=1,
                z=2,
                color="Dominant_Topic",
                title="3d TSNE Plot for Topic Model",
                opacity=0.7,
                width=900,
                height=800,
            )

            if system:
                if display_format == "streamlit":
                    st.write(fig)
                else:
                    fig.show()

            logger.info("Visual Rendered Successfully")

            if save:
                if not isinstance(save, bool):
                    plot_filename = os.path.join(save, "TSNE.html")
                else:
                    plot_filename = "TSNE.html"
                logger.info(f"Saving '{plot_filename}'")
                fig.write_html(plot_filename)


        elif plot == "topic_model":

            import pyLDAvis
            import pyLDAvis.gensim  # don't skip this

            import warnings
            from gensim.corpora import Dictionary


            def convertldaGenToldaMallet(mallet_model):
                model_gensim = LdaModel(
                    id2word=mallet_model.id2word, num_topics=mallet_model.num_topics,
                    alpha=mallet_model.alpha, eta=0,
                )
                model_gensim.state.sstats[...] = mallet_model.wordtopics
                model_gensim.sync_state()
                return model_gensim


            warnings.filterwarnings("ignore")
#            if self.verbose:
            pyLDAvis.enable_notebook()
            logger.info("Preparing pyLDAvis visual")
            from gensim.models.ldamodel import LdaModel
            vis = pyLDAvis.gensim.prepare(convertldaGenToldaMallet(self._model.model), self._model.corpus, dictionary=self._model.indexer, mds="mmds")
            if self.verbose:
                display(vis)
            else:

                pyLDAvis.show(vis)
            logger.info("Visual Rendered Successfully")


        elif plot == "topic_distribution":

            try:

                iter1 = len(self._model.show_topics(999999))

            except:

                try:
                    iter1 = self._model.num_topics

                except:

                    iter1 = self._model.n_components_

            topic_name = []
            keywords = []

            for i in range(0, iter1):

                try:

                    s = self._model.show_topic(i, topn=10)
                    topic_name.append("Topic " + str(i))

                    kw = []

                    for i in s:
                        kw.append(i[0])

                    keywords.append(kw)

                except:

                    keywords.append("NA")
                    topic_name.append("Topic " + str(i))

            keyword = []
            for i in keywords:
                b = ", ".join(i)
                keyword.append(b)

            kw_df = pd.DataFrame({"Topic": topic_name, "Keyword": keyword}).set_index(
                "Topic"
            )
            logger.info(
                "SubProcess predict() called =================================="
            )
            ass_df = self.model_interpreter.predict([v for v in self.data[self.target].values if v is not None], verbose=False)
            logger.info("SubProcess predict() end ==================================")
            ass_df_pivot = ass_df.pivot_table(
                index="Dominant_Topic", values="Topic_0", aggfunc="count"
            )
            df2 = ass_df_pivot.join(kw_df)
            df2 = df2.reset_index()
            df2.columns = ["Topic", "Documents", "Keyword"]

            """
            sorting column starts

            """

            logger.info("Sorting Dataframe")

            topic_list = list(df2["Topic"])

            s = []
            for i in range(0, len(topic_list)):
                a = int(topic_list[i].split()[1])
                s.append(a)

            df2["Topic"] = s
            df2.sort_values(by="Topic", inplace=True)
            df2.sort_values(by="Topic", inplace=True)
            topic_list = list(df2["Topic"])
            topic_list = list(df2["Topic"])
            s = []
            for i in topic_list:
                a = "Topic " + str(i)
                s.append(a)

            df2["Topic"] = s
            df2.reset_index(drop=True, inplace=True)

            """
            sorting column ends
            """

            logger.info("Rendering Visual")

            import plotly.express as px

            fig = px.bar(
                df2,
                x="Topic",
                y="Documents",
                hover_data=["Keyword"],
                title="Document Distribution by Topics",
            )

            if system:
                if display_format == "streamlit":
                    st.write(fig)
                else:
                    fig.show()

            logger.info("Visual Rendered Successfully")

            if save:
                if not isinstance(save, bool):
                    plot_filename = os.path.join(save, "Topic Distribution.html")
                else:
                    plot_filename = "Topic Distribution.html"
                logger.info(f"Saving '{plot_filename}'")
                fig.write_html(plot_filename)

        elif plot == "wordcloud":

            try:

                from wordcloud import WordCloud
                import matplotlib.pyplot as plt

                stopwords = set(get_stop_words(self.defaults["language"]))

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    atext = " ".join(review for review in self.data[self.target])

                else:

                    logger.info(
                        "SubProcess predict() called =================================="
                    )
                    assigned_df = self([v for v in self.data[self.target].values if v is not None])
                    assigned_df[self.target]=self.data[self.target]

                    logger.info(
                        "SubProcess predict() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    atext = " ".join(review for review in filtered_df[self.target])

                logger.info("Fitting WordCloud()")
                wordcloud = WordCloud(
                    width=800,
                    height=800,
                    background_color="white",
                    stopwords=stopwords,
                    min_font_size=10,
                ).generate(atext)

                # plot the WordCloud image
                plt.figure(figsize=(8, 8), facecolor=None)
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)

                logger.info("Rendering Visual")

                if save:
                    if system:
                        plt.savefig("Wordcloud.png")
                    else:
                        plt.savefig("Wordcloud.png")
                        plt.close()

                    logger.info("Saving 'Wordcloud.png' in current active directory")

                else:
                    if display_format == "streamlit":
                        st.write(plt)
                    else:
                        plt.show()

                logger.info("Visual Rendered Successfully")

            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        logger.info(
            "plot_model() succesfully completed......................................"
        )

