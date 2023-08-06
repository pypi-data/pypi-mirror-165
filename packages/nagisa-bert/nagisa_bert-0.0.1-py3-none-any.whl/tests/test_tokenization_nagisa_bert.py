from nagisa_bert.tokenization_nagisa_bert import NagisaBertTokenizer


class TestNagisaBertTokenizer:

    tokenizer = NagisaBertTokenizer.from_pretrained("taishi-i/nagisa_bert")

    text = "nagisaで[MASK]できるBERTモデルです"

    def test_vocab_size(self):
        expected_vocab_size = 60000
        assert expected_vocab_size == self.tokenizer.vocab_size

    def test_pad_token(self):
        expected_pad_token = "[PAD]"
        expected_pad_token_id = 0

        assert expected_pad_token == self.tokenizer.pad_token
        assert expected_pad_token_id == self.tokenizer.pad_token_id

    def test_unk_token(self):
        expected_unk_token = "[UNK]"
        expected_unk_token_id = 1

        assert expected_unk_token == self.tokenizer.unk_token
        assert expected_unk_token_id == self.tokenizer.unk_token_id

    def test_cls_token(self):
        expected_cls_token = "[CLS]"
        expected_cls_token_id = 2

        assert expected_cls_token == self.tokenizer.cls_token
        assert expected_cls_token_id == self.tokenizer.cls_token_id

    def test_sep_token(self):
        expected_sep_token = "[SEP]"
        expected_sep_token_id = 3

        assert expected_sep_token == self.tokenizer.sep_token
        assert expected_sep_token_id == self.tokenizer.sep_token_id

    def test_mask_token(self):
        expected_mask_token = "[MASK]"
        expected_mask_token_id = 4

        assert expected_mask_token == self.tokenizer.mask_token
        assert expected_mask_token_id == self.tokenizer.mask_token_id

    def test_space_token(self):
        expected_space_token_id = 5

        assert expected_space_token_id == self.tokenizer.convert_tokens_to_ids([" "])[0]

    def test_tokenize_basic(self):
        expected_tokens = [
            "n",
            "a",
            "g",
            "i",
            "s",
            "a",
            "で",
            "[MASK]",
            "できる",
            "b",
            "e",
            "r",
            "t",
            "モデル",
            "です",
        ]

        tokens = self.tokenizer.tokenize(self.text)
        assert expected_tokens == tokens

    def test_encode(self):
        expected_output = {
            "input_ids": [
                2,
                269,
                181,
                607,
                247,
                285,
                181,
                19,
                4,
                320,
                521,
                221,
                369,
                207,
                1629,
                63,
                3,
            ],
            "token_type_ids": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "attention_mask": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        }

        output = self.tokenizer(self.text)
        assert expected_output["input_ids"] == output["input_ids"]
        assert expected_output["token_type_ids"] == output["token_type_ids"]
        assert expected_output["attention_mask"] == output["attention_mask"]

    def test_convert_ids_to_tokens(self):
        output = self.tokenizer(self.text)

        expected_tokens = [
            "[CLS]",
            "n",
            "a",
            "g",
            "i",
            "s",
            "a",
            "で",
            "[MASK]",
            "できる",
            "b",
            "e",
            "r",
            "t",
            "モデル",
            "です",
            "[SEP]",
        ]

        tokens = self.tokenizer.convert_ids_to_tokens(output["input_ids"])
        assert expected_tokens == tokens
