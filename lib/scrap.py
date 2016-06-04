    from nolearn.lasagne import NeuralNet, BatchIterator
    from lasagne.layers import InputLayer as Input
    from lasagne.layers import DropoutLayer as Dropout
    from lasagne.layers import DenseLayer as Dense
    from lasagne.layers import RecurrentLayer as RNN
    from lasagne.layers import LSTMLayer as LSTM
    from lasagne.layers import GRULayer as GRU
    from lasagne.layers import ReshapeLayer as Reshape
    from lasagne.layers import EmbeddingLayer as Embedding
    from lasagne.layers import NonlinearityLayer as Nonlinearity
    from lasagne.nonlinearities import softmax
    from lasagne.objectives import categorical_crossentropy
    from lasagne.updates import adam


        elif 0:
            # TODO: consider using to_categorical instead
            #from keras.utils.np_utils import to_categorical
            x = np.array(seq_text[:newlen], dtype='int32').reshape((-1, seq_length))
            # Generate input and output per substring, as an indicator matrix.
            y = np.zeros((x.shape[0], x.shape[1], self.vocab_size), dtype='bool')
            for i in np.arange(x.shape[0]):
                for j in np.arange(x.shape[1]):
                    y[i, j, x[i, j]] = 1

            # push a padding character to the front of the inputs.
            # this effectively maps x[a,b,c]'s next character to y[a,b,c]
            x = np.roll(y, 1, axis=1)
            x[:, 0, :] = 0
            x[:, 0, 0] = 1

            vx = x
            vy = y
        else:
            # TODO: handle dtype more elegantly
            #vx = seq_text[0:newlen + 0]
            #vy = seq_text[1:newlen + 1]
            vy = seq_text[:newlen]
            vx = np.roll(vy, 1)
            vx[0] = 0 # remember we assert that 0 corresponds to PADDING in Translator

            # stuff in the original LanguageModel.lua that we don't need
            #vx = vx.reshape(batch_size, -1, self.seq_length)
            #vy = vy.reshape(batch_size, -1, self.seq_length)
            #vx = vx.transpose([1, 0, 2])
            #vy = vy.transpose([1, 0, 2])

            # this is good enough
            vx = vx.reshape(-1, self.seq_length)
            vy = vy.reshape(-1, self.seq_length)
            vx = np.array(vx, dtype=np.uint8)
            vy = np.array(vy, dtype=np.uint8)



    sentence = text[start_index:start_index + seq_length]
    generated = sentence
    lament('## Generating')
    sys.stdout.write(generated)
    sys.stdout.write('~') # PADDING

    was_pad = True
    for i in range(sample_chars):
        x = np.zeros((1, seq_length, textmap.vocab_size), dtype=np.bool)
        for t, char in enumerate(sentence):
            x[0, t, textmap.map(char)] = 1

        preds = model.predict(x, batch_size=1, verbose=0)[0]
        next_index = asample(preds, temperature)
        next_char = textmap.unmap(next_index)[0]

        generated += next_char
        sentence = sentence[1:] + next_char

        is_pad = next_char == PADDING
        sys.stdout.write(next_char)
        if is_pad and not was_pad:
            sys.stdout.write('\n')
        sys.stdout.flush()

        was_pad = is_pad
    lament()
