class VocabDict(object):
    def __init__(self, name = ""):
        self.name = name
        self.word2idx = {}
        self.word2count = {}
        self.idx2word = {}
        self.num_words = 0
    
    def add_words(self, word : str):
        if word not in self.word2idx:
            self.word2idx[word] = self.num_words
            self.word2count[word] = 1
            self.idx2word[self.num_words] = word
            self.num_words +=1
        else:
            self.word2count[word] +=1

    def to_word(self, idx : int):
        return self.idx2word[idx]
    
    def to_idx(self, word : str):
        return self.word2idx[word]
    
    