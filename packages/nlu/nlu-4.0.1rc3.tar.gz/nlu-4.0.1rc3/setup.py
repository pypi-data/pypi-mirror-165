from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

REQUIRED_PKGS = [
    'spark-nlp>=4.1.0,<4.2.0',
    'numpy',
    'pyarrow>=0.16.0',
    'pandas>=1.3.5',
    'dataclasses'
]

setup(
    name='nlu',
    version='4.0.1rc3',
    description='John Snow Labs NLU provides state of the art algorithms for NLP&NLU with 5000+ of pretrained models in 200+ languages. It enables swift and simple development and research with its powerful Pythonic and Keras inspired API. It is powerd by John Snow Labs powerful Spark NLP library.',

    long_description=long_description,
    install_requires=REQUIRED_PKGS,
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='http://nlu.johnsnowlabs.com',  # Optional
    author='John Snow Labs',  # Optional
    author_email='christian@johnsnowlabs.com',
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='NLP spark development NLU ',


    packages=find_packages(exclude=['test*', 'tmp*']),  # exclude=['test']
    data_files=[
        # classifiers
        ('', ['nlu/components/classifiers/classifier_dl/component_infos.json']),
        ('', ['nlu/components/classifiers/language_detector/component_infos.json']),
        ('', ['nlu/components/classifiers/named_entity_recognizer_crf/component_infos.json']),
        ('', ['nlu/components/classifiers/ner/component_infos.json']),
        ('', ['nlu/components/classifiers/pos/component_infos.json']),
        ('', ['nlu/components/classifiers/sentiment_detector/component_infos.json']),
        ('', ['nlu/components/classifiers/sentiment_dl/component_infos.json']),
        ('', ['nlu/components/classifiers/vivekn_sentiment/component_infos.json']),
        ('', ['nlu/components/classifiers/yake/component_infos.json']),
        ('', ['nlu/components/classifiers/multi_classifier/component_infos.json']),
        ('', ['nlu/components/classifiers/token_bert/component_infos.json']),
        ('', ['nlu/components/classifiers/token_albert/component_infos.json']),
        ('', ['nlu/components/classifiers/token_distilbert/component_infos.json']),
        ('', ['nlu/components/classifiers/token_longformer/component_infos.json']),
        ('', ['nlu/components/classifiers/token_roberta/component_infos.json']),
        ('', ['nlu/components/classifiers/token_xlm_roberta/component_infos.json']),
        ('', ['nlu/components/classifiers/token_xlnet/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_distilbert/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_bert/component_infos.json']),

        # dependency
        ('', ['nlu/components/dependency_typeds/labeled_dependency_parser/component_infos.json']),
        ('', ['nlu/components/dependency_untypeds/unlabeled_dependency_parser/component_infos.json']),

        # embeds
        ('', ['nlu/components/embeddings/elmo/component_infos.json']),
        ('', ['nlu/components/embeddings/albert/component_infos.json']),
        ('', ['nlu/components/embeddings/bert/component_infos.json']),
        ('', ['nlu/components/embeddings/glove/component_infos.json']),
        ('', ['nlu/components/embeddings/xlnet/component_infos.json']),
        ('', ['nlu/components/embeddings/use/component_infos.json']),
        ('', ['nlu/components/embeddings/sentence_bert/component_infos.json']),
        ('', ['nlu/components/embeddings/doc2vec/component_infos.json']),

        ('', ['nlu/components/embeddings/distil_bert/component_infos.json']),
        ('', ['nlu/components/embeddings/roberta/component_infos.json']),
        ('', ['nlu/components/embeddings/xlm/component_infos.json']),

        ('', ['nlu/components/embeddings/distil_bert/component_infos.json']),
        ('', ['nlu/components/embeddings/longformer/component_infos.json']),
        ('', ['nlu/components/embeddings/sentence_xlm/component_infos.json']),

        # Seq2Seq

        ('', ['nlu/components/seq2seqs/marian/component_infos.json']),
        ('', ['nlu/components/seq2seqs/t5/component_infos.json']),

        # lemma
        ('', ['nlu/components/lemmatizers/lemmatizer/component_infos.json']),

        # matcher
        ('', ['nlu/components/matchers/date_matcher/component_infos.json']),
        ('', ['nlu/components/matchers/regex_matcher/component_infos.json']),
        ('', ['nlu/components/matchers/text_matcher/component_infos.json']),
        ('', ['nlu/components/matchers/context_parser/component_infos.json']),

        # normalizer
        ('', ['nlu/components/normalizers/normalizer/component_infos.json']),
        ('', ['nlu/components/normalizers/document_normalizer/component_infos.json']),
        ('', ['nlu/components/normalizers/drug_normalizer/component_infos.json']),

        # sentence detector
        ('', ['nlu/components/sentence_detectors/deep_sentence_detector/component_infos.json']),
        ('', ['nlu/components/sentence_detectors/pragmatic_sentence_detector/component_infos.json']),

        # spell checker
        ('', ['nlu/components/spell_checkers/context_spell/component_infos.json']),
        ('', ['nlu/components/spell_checkers/norvig_spell/component_infos.json']),
        ('', ['nlu/components/spell_checkers/symmetric_spell/component_infos.json']),

        # stemmer
        ('', ['nlu/components/stemmers/stemmer/component_infos.json']),
        # tokenizer
        ('', ['nlu/components/tokenizers/default_tokenizer/component_infos.json']),
        ('', ['nlu/components/tokenizers/regex_tokenizer/component_infos.json']),
        ('', ['nlu/components/tokenizers/word_segmenter/component_infos.json']),

        # stopwords
        ('', ['nlu/components/stopwordscleaners/stopwordcleaner/component_infos.json']),

        # chunker
        ('', ['nlu/components/chunkers/default_chunker/component_infos.json']),
        ('', ['nlu/components/chunkers/ngram/component_infos.json']),
        ('', ['nlu/components/chunkers/contextual_parser/component_infos.json']),

        ('', ['nlu/components/embeddings_chunks/chunk_embedder/component_infos.json']),

        # utils
        ('', ['nlu/components/utils/chunk_2_doc/component_infos.json']),
        ('', ['nlu/components/utils/doc2chunk/component_infos.json']),
        ('', ['nlu/components/utils/deep_sentence_detector/component_infos.json']),
        ('', ['nlu/components/utils/document_assembler/component_infos.json']),
        ('', ['nlu/components/utils/sentence_detector/component_infos.json']),
        ('', ['nlu/components/utils/sentence_embeddings/component_infos.json']),
        ('', ['nlu/components/utils/ner_to_chunk_converter/component_infos.json']),
        ('', ['nlu/components/utils/chunk_merger/component_infos.json']),

        ('', ['nlu/components/utils/token_assembler/component_infos.json']),
        ('', ['nlu/components/deidentifiers/deidentifier/component_infos.json']),
        ('', ['nlu/components/relation_extractors/relation_extractor/component_infos.json']),
        ('', ['nlu/components/relation_extractors/relation_extractor_dl/component_infos.json']),
        ('', ['nlu/components/resolutions/chunk_entity_resolver/component_infos.json']),
        ('', ['nlu/components/resolutions/sentence_entity_resolver/component_infos.json']),
        ('', ['nlu/components/assertions/assertion_dl/component_infos.json']),
        ('', ['nlu/components/assertions/assertion_log_reg/component_infos.json']),
        ('', ['nlu/components/classifiers/generic_classifier/component_infos.json']),
        ('', ['nlu/components/utils/feature_assembler/component_infos.json']),
        ('', ['nlu/components/classifiers/ner_healthcare/component_infos.json']),
        ('', ['nlu/components/utils/ner_to_chunk_converter_licensed/component_infos.json']),

        ('', ['nlu/components/seq2seqs/gpt2/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_albert/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_roberta/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_longformer/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_xlm_roberta/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_xlnet/component_infos.json']),
        ('', ['nlu/components/classifiers/token_bert_healthcare/component_infos.json']),
        ('', ['nlu/components/classifiers/token_bert_healthcare/component_infos.json']),
        ('', ['nlu/components/embeddings/doc2vec/component_infos.json']),
        ('', ['nlu/components/embeddings/word2vec/component_infos.json']),
        ('', ['nlu/components/embeddings/deberta/component_infos.json']),

        ('', ['nlu/components/classifiers/seq_bert_medical/component_infos.json']),
        ('', ['nlu/components/classifiers/seq_distilbert_medical/component_infos.json']),
        #

    ],

    include_package_data=True  # Needed to install jar file

)
