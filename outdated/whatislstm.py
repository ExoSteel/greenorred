import torch
import torch.nn as nn

class SentLSTM(nn.Module):
    def __init__(self, vocab_size, tag_vocab_size, embedded_dim, tag_dim, hidden_dim):
        super().__init__()
        self.word_embeddings = nn.Embedding(vocab_size, embedded_dim)
        self.tag_embeddings = nn.Embedding(tag_vocab_size, tag_dim)

        self.lstm = nn.LSTM(embedded_dim + tag_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1) # Yes or No

    def forward(self, words, tags):
        w_emb = self.word_embeddings(words)
        t_emb = self.tag_embeddings(tags)
        
        x = torch.cat((w_emb, t_emb), dim=2)

        _, (hidden, _) = self.lstm(x)

        x = torch.sigmoid(self.fc(hidden[-1]))
        return x
