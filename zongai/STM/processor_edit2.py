# -*- coding: utf-8 -*-

import json
import random
import csv
import os


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None, text_c=None):
        """Constructs a InputExample.

        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.text_c = text_c
        self.label = label


class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r") as f:
            reader = json.load(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                lines.append(line)
            return lines

def Nan_handler(data):    
    if not data["options-for-correct-answers"]:
        data["options-for-correct-answers"] = [{
                "candidate-id": '0',
                "speaker": "unknown",
                "utterance": "unknown"
            }]
        data["options-for-next"].insert(0,{
                "candidate-id": '0',
                "utterance": "unknown"
            })
        data["options-for-next"].pop()
    return data

class UbuntuProcessor(DataProcessor):
    def __init__(self):
        self.D = []

        for sid in range(3):
            with open([os.path.join(os.getcwd(), "dataset/DSTC8/task-2.ubuntu.train.json"),
                       os.path.join(os.getcwd(), "dataset/DSTC8/task-2.ubuntu.dev.json"),
                       os.path.join(os.getcwd(), "dataset/DSTC8/task-2.ubuntu.test.blind.json")][sid], "r") as f:
                data = json.load(f)
                self.D.append(data)

    def get_train_examples(self):
        """See base class."""
        return self._create_examples(
            self.D[0], "train")

    def get_test_examples(self):
        """See base class."""
        return self._create_examples(
            self.D[2], "test")

    def get_dev_examples(self):
        """See base class."""
        return self._create_examples(
            self.D[1], "dev")

    def _create_examples(self, data, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, d) in enumerate(data):
            d = Nan_handler(d)
            context = []
            candiates = []
            label = None
            if set_type == 'train':
                if i in range(1000000):
                    for t in d['messages-so-far']:
                        context.append(t['utterance'])
                    ground_truth = d['options-for-correct-answers'][0]['candidate-id']
                    for c_id, c in enumerate(d['options-for-next']):
                        candiates.append(c['utterance'])
                        if c['candidate-id'] == ground_truth:
                            label = c_id 
                    guid = "%s-%s" % (set_type, d['example-id'])
                    examples.append(InputExample(guid=guid, text_a=context, text_b=candiates, label=label))
            if set_type == 'dev':
                if i in range(1000000):
                    for t in d['messages-so-far']:
                        context.append(t['utterance'])
                    ground_truth = d['options-for-correct-answers'][0]['candidate-id']
                    for c_id, c in enumerate(d['options-for-next']):
                        candiates.append(c['utterance'])
                        if c['candidate-id'] == ground_truth:
                            label = c_id                    
                    guid = "%s-%s" % (set_type, d['example-id'])
                    examples.append(InputExample(guid=guid, text_a=context, text_b=candiates, label=label))
            if set_type == 'test':
                if i in range(1):
                    for t in d['messages-so-far']:
                        context.append(t['utterance'])
                    ground_truth = d['options-for-correct-answers'][0]['candidate-id']
                    for c_id, c in enumerate(d['options-for-next']):
                        candiates.append(c['utterance'])
                        if c['candidate-id'] == ground_truth:
                            label = c_id                    
                    guid = "%s-%s" % (set_type, d['example-id'])
                    examples.append(InputExample(guid=guid, text_a=context, text_b=candiates, label=label))
                    
        return examples
