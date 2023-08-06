from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Dict, Generic, Iterable, List, Sequence, Tuple, TypeVar, Union
)

import numpy as np
import numpy.typing as npt

from truera.client.nn import BaselineLike
from truera.client.nn import BaselineType
from truera.client.nn import Batch
from truera.client.nn import NNBackend as NNB
from truera.client.nn.wrappers import Base
from truera.client.nn.wrappers import DataBatch
from truera.client.nn.wrappers import InputBatch
from truera.client.nn.wrappers import Wrapping
from truera.client.util.func_utils import Deprecate
from truera.client.util.func_utils import WrapperMeta


class NLP(Base):
    """
    Wrappers for NLP models. In addition to base wrappers, NLP requires a
    tokenizer wrapper. The tokenizer is responsible for final preparation of
    text (string) instaces into the appropriate form accepted by the model.
    Other additions/changes over base wrappers are:

        `ModelLoadWrapper`

        - `__init__` - each wrapper's initializer must call
          `NLP.ModelLoadWrapper`'s initializer specifying `n_tokens` and
          `n_embeddings`, integers indicating the maximum number of tokens the
          model accepts per input instance, and how large is its embedding
          space.

        - `get_tokenizer` - new method loads/retrieves the tokenizer wrapper.

        `ModelRunWrapper`

        - `evaluate_model` now takes in a tokenizer wrapper and must perform the
          required tokenzation to prepare a data batch for the model.

        - `ds_elements_to_truera_elements` does the same and must process a
          databatch to extract the additional fields `TruBatch` (see
          `NLP.TruBatch`) requires.

        `SplitLoadWrapper`

        - no changes from base version
    """

    # NLP.TokenizerWrapper related types
    Text = str
    TokenId = int
    Token = str
    Word = str
    Part = TypeVar("Part", Token, Word)

    # TextBatch = npt.NDArray[Text]

    @dataclass
    class TruBatch(Batch):
        index: npt.NDArray[np.long] = Batch.field(np.array)  # (batch)
        labels: npt.NDArray[np.int] = Batch.field(np.array)  # (batch)
        # token_ids: npt.NDArray[NLP.TokenId] = Batch.field(
        #    np.array
        #)  # (batch x text length in tokens)
        #attention_mask: npt.NDArray[np.int] = Batch.field(
        #    np.array
        #)  # (batch x text length in tokens)
        original_text: npt.NDArray[NLP.Text] = Batch.field(np.array)  # (batch)
        processed_text: npt.NDArray[NLP.Text] = Batch.field(np.array)  # (batch)

    TextBatch = Iterable[Text]

    @dataclass
    class Span(Generic[Part]):
        """
        Tokens or words along with indices into the string from which they were
        derived.
        """

        item: NLP.Part
        begin: int
        end: int

        @staticmethod
        def of_hugs(
            pair: Tuple[NLP.Part, Tuple[int, int]]
        ) -> NLP.Span[NLP.Part]:
            """
            Convert some structures returned by huggingface parsers/tokenizers into
            a span.
            """
            return NLP.Span(item=pair[0], begin=pair[1][0], end=pair[1][1])

    TokenLike = Union[
        Token,
        TokenId]  # tokens are either their readable string or integer index.

    # Outputs of tokenizers that are sent directly to models as inputs.
    Tokenization = TypeVar("Tokenization")

    @dataclass
    class TruTokenization(Generic[Part]):
        """
        Outputs of tokenizers used for various aggregation and display purposes.
        """

        spans: Iterable[Iterable[NLP.Span[NLP.Part]]]
        token_ids: npt.NDArray[np.int] = None  # when Part=Token
        attention_mask: npt.NDArray[np.int] = None  # when Part=Token

    # Can only mix into TokenizerWrapper
    class WithTokenizerWrapperOptional:
        """
        Optional methods to customize some aspects of an NLP analysis. The
        methods defined here come with sensible/noop defaults but can be
        extended in a subclass for alternate behaviour.
        """

        @Wrapping.optional
        def tokenize_into_tru_words(
            self, texts: Iterable[NLP.Text]
        ) -> NLP.TruTokenization[NLP.Word]:
            """
            Split a set of texts, each, into their constituent words. Each
            returned word must come with spanning information into its origin
            string with begining and end indices.

            Default implementation is a whitespace-based splitter using
            huggingface's tokenizers.pre_tokenizers.Whitespace .
            """

            sentences = [
                self._word_splitter.pre_tokenize_str(text) for text in texts  # pylint: disable=E1101
            ]

            return NLP.TruTokenization(
                spans=[
                    [NLP.Span.of_hugs(p)
                     for p in sentence]
                    for sentence in sentences
                ]
            )

        @Wrapping.optional
        def visible_token(self, token: NLP.Token) -> str:
            """
            Render the token for interactive user.
            
            Transformers' BertTokenizer has these hashes in some tokens which
            can be removed for visualiztions:

            ```
                if token[:2] == "##":
                    token = token[2:]
                elif token[-2:] == "##":
                    token = token[:-2]
            ```
            """

            return token

        @Wrapping.optional
        def visible_word(self, word: NLP.Word) -> str:
            """
            Render the word for interactive user.
            """
            return word

    # Can only mix into TokenizerWrapper
    class WithTokenizerWrapperUtility:
        """
        Utility methods for helping you with your tokenizer wrapper. These
        cannot be overridden by your wrapper but can be used to simplify
        its construction.
        """

        @Wrapping.utility
        @property
        def model_path(self) -> Path:
            return self._model_path  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def vocab(self) -> Dict[NLP.Token, NLP.TokenId]:
            return self._vocab  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def vocab_inverse(self) -> Dict[NLP.Token, NLP.TokenId]:
            return self._vocab_inverse  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def n_tokens(self) -> int:
            """
            Number of tokens a wrapped model expects. This should be
            retrieved from ModelLoadWrapper.
            """
            return self._n_tokens

        @n_tokens.setter
        def n_tokens(self, val: int) -> None:
            self._n_tokens = val

        @Wrapping.utility
        def _add_special_token_ids(self, ids: Iterable[NLP.TokenId]) -> None:
            self._special_token_ids += ids  # pylint: disable=E1101
            self._special_tokens += [self.token_of_id(id) for id in ids]  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def special_tokens(self) -> List[NLP.TokenId]:
            return self._special_tokens  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def special_token_ids(self):
            return self._special_token_ids  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def unk_token_id(self) -> NLP.TokenId:
            return self._unk_token_id  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def pad_token_id(self) -> NLP.TokenId:
            return self._pad_token_id  # pylint: disable=E1101

        @Wrapping.utility
        def tokens_of_text(self, text: NLP.Text) -> List[NLP.Span[NLP.Token]]:
            return self.tokens_of_texts([text])[0]  # pylint: disable=E1101

        @Wrapping.utility
        def words_of_text(self, text: NLP.Text) -> List[NLP.Span[NLP.Word]]:
            return self.words_of_texts([text])[0]  # pylint: disable=E1101

        @Wrapping.utility
        def ids_of_tokens(self,
                          tokens: Iterable[NLP.Token]) -> Iterable[NLP.TokenId]:
            """
            Given tokens' string representations, produce their ids.
            """
            return [
                self.vocab[token] if token in self.vocab else self.unk_token_id
                for token in tokens
            ]

        @Wrapping.utility
        def id_of_token(self, token: NLP.Token) -> NLP.TokenId:
            return self.ids_of_tokens([token])[0]

        @Wrapping.utility
        def tokens_of_ids(self,
                          ids: Iterable[NLP.TokenId]) -> Iterable[NLP.Token]:
            """
            Given a sequence of token ids, produce the corresponding sequence of
            tokens as strings.
            """
            return [self.vocab_inverse[token_id] for token_id in ids]

        @Wrapping.utility
        def token_of_id(self, id: NLP.TokenId) -> NLP.Token:
            return self.tokens_of_ids([id])[0]

        @Wrapping.utility
        def id_of_tokenlike(self, tokenlike: NLP.TokenLike) -> NLP.TokenId:
            # TODO: remove from here, move to attribution setup stuff
            """
            TokenLike = Union[Token, TokenId]
            """

            if isinstance(tokenlike, str):
                return self.id_of_token(tokenlike)
            elif isinstance(tokenlike, int):
                return tokenlike
            else:
                raise ValueError(
                    f"Unhandled type ({type(tokenlike)}) of tokenlike {tokenlike}."
                )

    class TokenizerWrapper(
        WithTokenizerWrapperOptional,
        WithTokenizerWrapperUtility,
        metaclass=WrapperMeta
    ):
        """
        Tokenizers split text inputs (sentences, paragraphs, documents, or other
        NLP model inputs) into tokens that can be fed into an NLP model.

        Tokenizer operates on four types of objects. Text strings, integer token
        ids, string tokens and string words. For some models or tokenizers,
        tokens and words are the same.

        Relevant types:
         - Text = str
         - TokenId = int
         - Token = str
         - Word = str
         - Part <= Token | Word
         - Span of item: Part, begin: int, end: int
        """

        @Wrapping.require_init
        def __init__(
            self, model_path: Path, vocab: Dict[NLP.Token, NLP.TokenId],
            n_tokens: int, unk_token_id: int, pad_token_id: int, *args, **kwargs
        ):
            """
            Required args must be provided by sub-class.
            """

            self._model_path = model_path

            self._vocab: Dict[NLP.Token, NLP.TokenId] = vocab
            self._vocab_inverse = {i: t for t, i in self._vocab.items()}

            self._special_token_ids: List[NLP.TokenId] = []
            self._special_tokens: List[NLP.Token] = []

            self._unk_token_id: NLP.TokenId = unk_token_id
            self._pad_token_id: NLP.TokenId = pad_token_id

            self._add_special_token_ids([self.unk_token_id, self.pad_token_id])

            self._n_tokens: int = n_tokens

            # Whitespace tokenizer for default word splitting.
            import tokenizers
            self._word_splitter = tokenizers.pre_tokenizers.Whitespace()

        @Wrapping.required
        @abstractmethod
        def inputbatch_of_textbatch(
            self, texts: Iterable[NLP.Text]
        ) -> InputBatch:
            """
            Tokenize texts into a form that wrapped model expects.
            """
            ...

        @Wrapping.required
        @abstractmethod
        def tokenize_into_tru_tokens(
            self, texts: Iterable[NLP.Text]
        ) -> NLP.TruTokenization[NLP.Token]:
            """
            Tokenize texts and report several fields:
                - spans -- the spans which include token names and their begin/end indices
                - token_ids -- the corresponding token_id's
                - attention_mask -- indicator of which tokens are not pad
            
            Example for Huggingface's BertTokenizerFast:
            ```
            parts = bert_tokenizer
                .batch_encode_plus(
                    texts,
                    return_offsets_mapping=True, # required for spans
                    return_token_type_ids=False, # don't need these
                    return_attention_mask=True   # require for TruTokenization
                )
            input_idss: npt.NDArray[np.int] = parts['input_ids']
            attention_maskss = npt.NDArray[np.int] = parts['attention_mask]

            tokenss = [bert_tokenizer.batch_decode(input_ids) for input_ids in input_idss]
            offsetss = parts['offset_mapping']
            
            spanss = [
                [
                    NLP.Span(item=t, begin=o[0], end=o[1])
                    for t, o in zip(tokens, offsets)
                ]
                for tokens, offsets in zip(tokenss, offsetss)
            ]

            return NLP.TruTokenization(
                spans=spanss,
                token_ids=np.ndarray(input_idss),
                attention_mask=np.ndarray(attention_maskss)
            )
            ```
            """
            pass

    class WithModelLoadWrapperUtility:

        @Wrapping.utility
        def print_layer_names(self, model: NNB.Model) -> None:
            """Print layer names in the given model."""

            from trulens.nn.models import get_model_wrapper

            wrapper = get_model_wrapper(model)
            wrapper.print_layer_names()

        @Wrapping.utility
        @property
        def n_tokens(self) -> int:
            """Number of tokens the model expects."""
            return self._n_tokens  # pylint: disable=E1101

        @Wrapping.utility
        @property
        def n_embeddings(self) -> int:
            """Number of dimensions in a token's embedding."""
            return self._n_embeddings  # pylint: disable=E1101

    class ModelLoadWrapper(Base.ModelLoadWrapper, WithModelLoadWrapperUtility):
        """Model load wrapper for NLP models."""

        @Wrapping.required
        @abstractmethod
        def get_tokenizer(self, n_tokens: int = None) -> NLP.TokenizerWrapper:
            """
            Return the tokenizer which converts a string into token ids. If the
            tokenizer needs to be loaded from a path, then it will be assumed to
            be available at location indicated by get_code_path.
            
            Args:
            - n_tokens: int - the number of tokens the model expects in its
              input.

            Output
            ----------------
            - A tokenizer wrapper.
            ----------------
            """
            ...

    class ModelRunWrapper(Base.ModelRunWrapper):
        """Run wrapper for NLP models."""

        @Wrapping.require_init_if_extended
        def __init__(self, n_tokens: int, n_embeddings: int):
            """
            Initalize required parameters of an NLP ModelRunWrapper.

            - n_tokens: int - the number of tokens the model expects in its
              input.
            - n_embeddings: int - the dimensions in token embeddings used in
              this model.

            Your implementation will need to be called with n_tokens and n_embeddings
            in the __init__() method

            ``` 
            def __init__(self, n_tokens, n_embeddings):
                super().__init__(n_tokens=n_tokens, n_embeddings=n_embeddings)
            ```
            
            """
            # Child classes will have to initialize us by giving us these required parameters.
            super().__init__()
            self._n_tokens = n_tokens
            self._n_embeddings = n_embeddings

        @Wrapping.utility
        @classmethod
        def inputbatch_of_textbatch(
            cls, texts: Iterable[NLP.Text], *, model: NNB.Model,
            tokenizer: NLP.TokenizerWrapper
        ) -> Base.InputBatch:
            return tokenizer.inputbatch_of_textbatch(texts)

        @Wrapping.deprecates(
            "ds_elements_to_truera_elements",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        @staticmethod
        @abstractmethod
        def trubatch_of_databatch(
            databatch: DataBatch, *, model: NNB.Model,
            tokenizer: NLP.TokenizerWrapper
        ) -> NLP.TruBatch:
            """Same as Timeseries version except different fields are required:
            
            - ids = array of size (batch x 1) : <ids to pair with records>
            - labels = array of size (batch x 1) : <label of each record>
            - original_text = TODO
            - processed_text = TODO

            Input
            ----------------
            - databatch: the output of a single iteration over the
              DataWrapper.get_ds object
            - model: the model object. This may be needed if the model does any
              preprocessing.
            - tokenizer: tokenizer wrapper in case it is needed
            ----------------
            Output
            ----------------
            - TruBatch: contents of databatch but in tru form.
            ----------------
            """
            ...

        # Temporary for trulens integration.
        @staticmethod
        # @abstractmethod
        def get_tru_baseline(
            model: NNB.Model,
            *,
            tokenizer: NLP.TokenizerWrapper,
            ref_token: NLP.TokenLike = '[PAD]',
            baseline_type: BaselineType = BaselineType.FIXED,
            fixed_baseline: NNB.Tensor = None,
            # attention_mask=None
        ) -> BaselineLike:
            ...

        @Wrapping.utility
        @property
        def n_tokens(self) -> int:
            """Number of tokens the model expects."""
            return self._n_tokens

        @Wrapping.utility
        @property
        def n_embeddings(self) -> int:
            """Number of dimensions in a token's embedding."""
            return self._n_embeddings

        @Wrapping.utility
        @classmethod
        def textbatch_of_trubatch(
            cls, trubatch: DataBatch, *, model: NNB.Model,
            tokenizer: NLP.TokenizerWrapper
        ) -> NLP.TextBatch:
            return list(trubatch.original_text)

        @Wrapping.utility
        @classmethod
        def textbatch_of_databatch(
            cls, databatch: DataBatch, *, model: NNB.Model,
            tokenizer: NLP.TokenizerWrapper
        ) -> NLP.TextBatch:
            trubatch = cls.trubatch_of_databatch(
                databatch, model=model, tokenizer=tokenizer
            )
            return cls.textbatch_of_trubatch(
                trubatch, model=model, tokenizer=tokenizer
            )

        @Wrapping.utility
        @classmethod
        def inputbatch_of_databatch(
            cls, databatch: DataBatch, *, model: NNB.Model,
            tokenizer: NLP.TokenizerWrapper
        ) -> InputBatch:
            kw = dict(model=model, tokenizer=tokenizer)
            trubatch = cls.trubatch_of_databatch(databatch, **kw)
            textbatch = cls.textbatch_of_trubatch(trubatch, **kw)
            inputbatch = cls.inputbatch_of_textbatch(list(textbatch), **kw)
            return inputbatch

        # Utility, do not override. Method intended for single text instances.
        @Wrapping.utility
        @classmethod
        def evaluate_model_from_text(
            cls, model: NNB.Model, text: NLP.Text,
            tokenizer: NLP.TokenizerWrapper
        ) -> Base.OutputBatch:
            return cls.evaluate_model_from_texts(model, [text], tokenizer)

        @Wrapping.utility
        @classmethod
        def evaluate_model_from_texts(
            cls, model: NNB.Model, texts: List[str],
            tokenizer: NLP.TokenizerWrapper
        ) -> Base.OutputBatch:
            """
            An evaluate model function where the input is in text format. No
            batching is performed here.

            Input
            ----------------
            - model: The model object
            - texts: The texts to evaluate.
            - tokenizer: a TokenizerWrapper object.
            ----------------
            Output
            ----------------
            - an array of probits.
            ----------------
            """

            inputs = cls.inputbatch_of_textbatch(
                texts=texts, model=model, tokenizer=tokenizer
            )

            return cls.evaluate_model(model=model, inputs=inputs)

        class WithEmbeddings(ABC):
            # NOTE(piotrm): for the trulens implementation, we need this to
            # define cuts for a distribution of interest.

            @staticmethod
            @abstractmethod
            def get_embeddings(
                model: NNB.Model, word_ids: NNB.Words
            ) -> NNB.Embeddings:
                """
                Produce embeddings for the given words. This intermediate model
                output may be necessary for some explanations when using the
                trulens explanations backend.
                """
                ...

    class SplitLoadWrapper(Base.SplitLoadWrapper):
        """Split load wrapper for NLP fairness data."""

        @Wrapping.required
        @abstractmethod
        def get_ds(
            self,
            batch_size: int = 4  # Lower default for NLP use case.
        ) -> Iterable[DataBatch]:
            ...

        class WithSegmentByWord(ABC):
            """Split load wrapper for NLP fairness segments data"""

            @staticmethod
            @abstractmethod
            def get_segment_keywords_map() -> Dict[str, Sequence[str]]:
                """
                [Optional] Only used if split loader is processing text
                inputs for segment metadata
                
                Args:
                    None: 
                Return:
                    segment_keywords_map: [Sequence[str]] a mapping from a
                    segment_name to keywords for text samples that
                    correspond to that segment
                """
                ...
