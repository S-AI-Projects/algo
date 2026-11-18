---

id: long-short-term-memory  
title: Long Short-Term Memory (LSTM)  
sidebar_label: LSTM  
description: "This post delves into Long Short-Term Memory (LSTM), a type of recurrent neural network designed to overcome the vanishing gradient problem, enabling better learning of long-term dependencies in sequential data."  
tags: [machine learning, deep learning, lstm, rnn, neural networks, time series, NLP]

---

### Definition:
**Long Short-Term Memory (LSTM)** is a special type of Recurrent Neural Network (RNN) architecture designed to learn long-term dependencies. It addresses the vanishing gradient problem inherent in vanilla RNNs by introducing gates that regulate the flow of information through the network. LSTMs are particularly effective for tasks involving sequential data, such as time-series prediction, language modeling, and speech recognition.

### Video Explanation

<LiteYouTubeEmbed
  id="YCzL96nL7j0"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Long Short-Term Memory (LSTM), Clearly Explained"
  lazyLoad={true}
  webp
/>

### Characteristics:
- **Gated Architecture**:  
  LSTMs utilize gates (input, forget, output) to control which information is remembered, forgotten, or passed on to the next time step. This allows them to maintain relevant information over long sequences.
  
- **Memory Cell**:  
  The key feature of an LSTM is the memory cell, which retains information over arbitrary time intervals. The network can decide whether to keep or discard information at each time step.

- **Efficient Learning of Long-term Dependencies**:  
  Unlike vanilla RNNs, which struggle to retain long-term dependencies due to the vanishing gradient problem, LSTMs are explicitly designed to remember information over longer time periods.

### Components of LSTM:
1. **Cell State**:  
   The cell state is the LSTM’s "memory," which flows through the network with only minor linear interactions. It retains information over long sequences.
  
2. **Forget Gate**:  
   The forget gate decides what information from the cell state should be discarded. It uses a sigmoid function to output values between 0 and 1, where 0 means "completely forget" and 1 means "completely retain."

3. **Input Gate**:  
   The input gate controls which new information should be stored in the cell state. It consists of a sigmoid layer that decides which values to update and a tanh layer that creates new candidate values for updating the cell state.

4. **Output Gate**:  
   The output gate determines the output of the LSTM at each time step. It uses the updated cell state to compute the next hidden state, which is passed on to the next time step.

5. **Hidden State**:  
   The hidden state is the output of the LSTM for the current time step. It’s influenced by the output gate and the updated cell state.

### LSTM Architecture:
1. **Input Layer**:  
   Sequential data (e.g., words in a sentence, time-series data) is provided as input to the LSTM one time step at a time.

2. **LSTM Cell**:  
   Each time step is processed by an LSTM cell, which updates the hidden state and cell state based on the current input, the previous hidden state, and the previous cell state.

3. **Output Layer**:  
   The output can be generated at each time step (e.g., language translation or generation tasks) or after processing the entire sequence (e.g., sentiment analysis or time-series prediction).

### Types of LSTMs:
1. **Vanilla LSTM**:  
   The most basic form of LSTM, where information flows sequentially through the input, forget, and output gates for each time step.

2. **Bidirectional LSTM (BiLSTM)**:  
   This architecture consists of two LSTM layers that process the input in both forward and backward directions. It is especially useful for tasks where future context is as important as past context.

3. **Stacked LSTM**:  
   Multiple LSTM layers are stacked on top of each other, enabling the network to learn more complex and hierarchical patterns in the data.

4. **Peephole LSTM**:  
   In Peephole LSTMs, the gates also receive input from the cell state, allowing them to "peek" into the cell state during updates.

### Problem Statement:
Given sequential data such as time-series, text, or audio, the goal of an LSTM is to make accurate predictions by effectively capturing long-term dependencies while mitigating issues like vanishing gradients.

### Key Concepts:
- **Memory Cell**:  
  LSTMs maintain a memory cell that persists over time and can store relevant information while discarding irrelevant information through its gates.

- **Vanishing Gradient Problem**:  
  LSTMs help mitigate the vanishing gradient problem in vanilla RNNs, which makes them better suited for learning long-term dependencies.

- **Gates**:  
  LSTMs employ three main gates (forget, input, and output gates) to regulate the flow of information, ensuring that important information is remembered and unimportant information is forgotten.

- **Backpropagation Through Time (BPTT)**:  
  LSTMs use BPTT to update weights by propagating gradients back through the entire sequence. Due to the gating mechanism, LSTMs avoid the vanishing gradient problem better than traditional RNNs.

### Steps Involved:
1. **Input Data**:  
   Sequential data is fed into the LSTM one time step at a time.

2. **Gate Calculations**:  
   The forget, input, and output gates compute which information to retain, update, and output at each time step.

3. **Cell State Update**:  
   The cell state is updated using the information from the forget and input gates, deciding which information to keep or discard.

4. **Hidden State Calculation**:  
   The output gate computes the hidden state, which is used as the output for the current time step and passed to the next LSTM cell.

5. **Final Output**:  
   After processing the entire sequence, the final hidden state can be used for tasks like sequence classification, or intermediate outputs can be used for tasks like sequence generation.

### Split Criteria:
LSTMs process data in sequential order, using the previous hidden state and cell state at each time step to inform the current step’s calculations. They are particularly useful for tasks where maintaining information over long sequences is critical.

### Time Complexity:
- **Training Complexity**:  
  The time complexity of training an LSTM is proportional to the sequence length $T$, the size of the input $n$, and the number of hidden units $h$, and is approximately $O(T \cdot n \cdot h^2)$.

- **Prediction Complexity**:  
  For inference, the complexity depends on the sequence length, as LSTMs must process each time step sequentially.

### Space Complexity:
- **Space Complexity**:  
  LSTMs need memory proportional to the sequence length $T$ and the number of hidden units $h$, resulting in a space complexity of $O(T \cdot h)$.

### Example:
Consider a deterministic, self-contained LSTM sentiment example using fixed seeds and sorted vocabulary indices:

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def build_vocab(text):
    # Sort unique characters to remove PYTHONHASHSEED-dependent set() order
    vocab = sorted(set(text))
    char_to_idx = {ch: idx for idx, ch in enumerate(vocab)}
    return vocab, char_to_idx


def encode_one_hot(text, char_to_idx):
    seq = np.zeros((len(text), len(char_to_idx)), dtype=np.float64)
    for t, ch in enumerate(text):
        seq[t, char_to_idx[ch]] = 1.0
    return seq


def run_lstm_sentiment(text, target=1.0, hidden_size=8, epochs=100, lr=0.1, seed=42):
    # Local seeded RNG avoids mutating process-global random state
    rng = np.random.default_rng(seed)
    vocab, char_to_idx = build_vocab(text)
    x_seq = encode_one_hot(text, char_to_idx)
    concat_size = hidden_size + len(vocab)

    Wf = rng.normal(0.0, 0.1, (concat_size, hidden_size))
    bf = np.zeros(hidden_size)
    Wi = rng.normal(0.0, 0.1, (concat_size, hidden_size))
    bi = np.zeros(hidden_size)
    Wc = rng.normal(0.0, 0.1, (concat_size, hidden_size))
    bc = np.zeros(hidden_size)
    Wo = rng.normal(0.0, 0.1, (concat_size, hidden_size))
    bo = np.zeros(hidden_size)
    Wy = rng.normal(0.0, 0.1, (hidden_size, 1))
    by = np.zeros(1)

    def forward(seq):
        h = np.zeros(hidden_size)
        c = np.zeros(hidden_size)
        for x_t in seq:
            z = np.concatenate([h, x_t])
            f_t = sigmoid(z @ Wf + bf)
            i_t = sigmoid(z @ Wi + bi)
            c_tilde = np.tanh(z @ Wc + bc)
            c = f_t * c + i_t * c_tilde
            o_t = sigmoid(z @ Wo + bo)
            h = o_t * np.tanh(c)
        return h, float(sigmoid(h @ Wy + by)[0])

    for _ in range(epochs):
        h_last, prob = forward(x_seq)
        grad = prob - target
        Wy -= lr * np.outer(h_last, [grad])
        by -= lr * grad

    _, final_prob = forward(x_seq)
    label = "Positive" if final_prob > 0.5 else "Negative"
    return vocab, [char_to_idx[ch] for ch in text], round(final_prob, 4), label


# Worked example with literal fixture from the article
text = "This movie was fantastic"
vocab, input_seq, prob, predicted_sentiment = run_lstm_sentiment(text, target=1.0, seed=42)
print(f"Vocabulary size: {len(vocab)}, First 5 sorted tokens: {vocab[:5]}")
print(f"Encoded sequence prefix: {input_seq[:6]}")
print(f"Predicted Probability: {prob:.4f}")
print(f"Predicted Sentiment: {predicted_sentiment}")

# Smallest valid boundary example (single time step, T = 1)
b_vocab, b_seq, b_prob, b_sentiment = run_lstm_sentiment("a", target=1.0, seed=42)
print(f"Boundary (T=1) vocab: {b_vocab}, seq: {b_seq}, prob: {b_prob:.4f}, sentiment: {b_sentiment}")
```

### Reproducibility & Boundary Case

- **Hidden State Removed:** Replacing `enumerate(set(text))` with `sorted(set(text))` eliminates dependence on Python's per-process `PYTHONHASHSEED`, and initializing weights via a local `np.random.default_rng(42)` generator avoids mutating process-global RNG state.
- **Concrete Intermediate State:** On `"This movie was fantastic"`, sorting the 15 unique characters yields `[' ', 'T', 'a', 'c', 'e', ...]` and maps the prefix `"This m"` deterministically to `[1, 6, 7, 11, 0, 8]`.
- **Boundary Case (`T = 1`):** Consistent with the time/space complexity contract ($T \ge 1$), a single-character sequence `"a"` executes one LSTM cell step (`vocab = ['a']`, `seq = [0]`) and converges to `"Positive"`.

### Example Output

```plaintext
Vocabulary size: 15, First 5 sorted tokens: [' ', 'T', 'a', 'c', 'e']
Encoded sequence prefix: [1, 6, 7, 11, 0, 8]
Predicted Probability: 0.8996
Predicted Sentiment: Positive
Boundary (T=1) vocab: ['a'], seq: [0], prob: 0.8993, sentiment: Positive
```

### Applications of LSTMs:
- **Natural Language Processing (NLP)**:  
  LSTMs are widely used in NLP tasks such as text generation, language translation, and sentiment analysis due to their ability to capture long-term dependencies in text.

- **Time-series Forecasting**:  
  LSTMs can predict future values in time-series data, making them valuable for financial forecasting, stock price prediction, and weather forecasting.

- **Speech Recognition**:  
  LSTMs process sequential audio data to recognize speech patterns and convert them into text.

- **Music Generation**:  
  LSTMs can generate new music by learning patterns from existing music sequences.

- **Video Analysis**:  
  LSTMs can analyze video sequences by processing frames in order and learning patterns over time.

### Conclusion:
Long Short-Term Memory (LSTM) networks are a powerful type of recurrent neural network that can capture long-term dependencies in sequential data. With their gated architecture, LSTMs overcome the vanishing
