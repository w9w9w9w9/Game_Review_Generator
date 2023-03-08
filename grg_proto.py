import numpy as np
import pickle
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub

# 데이터셋 로드 및 전처리
with open('test.pkl', 'rb') as f:
    reviews = pickle.load(f)

# FastText 임베딩 모델 로드
embedding_model = hub.load('https://tfhub.dev/google/fasttext/1')
text_embedding = embedding_model(reviews).numpy()

# 입력 시퀀스와 타겟 시퀀스 생성
seq_length = 50
sequences = []
for i in range(seq_length, len(text_embedding)):
    seq = text_embedding[i-seq_length:i]
    target = text_embedding[i]
    sequences.append((seq, target))

# 데이터셋 분할 및 배치 처리
batch_size = 32
num_batches = len(sequences) // batch_size
data = tf.data.Dataset.from_generator(lambda: sequences, output_types=(tf.float32, tf.float32))
data = data.shuffle(len(sequences)).batch(batch_size)

# 모델 정의
model = keras.Sequential([
    keras.layers.Input(shape=(seq_length, 300)),
    keras.layers.LSTM(256, return_sequences=True),
    keras.layers.Dropout(0.2),
    keras.layers.LSTM(256),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(300, activation='linear')
])

optimizer = keras.optimizers.Adam(lr=0.001)
model.compile(optimizer=optimizer, loss='mse')

# 모델 학습
num_epochs = 10
for epoch in range(num_epochs):
    loss = 0
    for batch in data:
        X, y = batch
        loss += model.train_on_batch(X, y)
    print('Epoch:', epoch+1, 'Loss:', loss/num_batches)

# 텍스트 생성
start_text = 'shall i compare thee to a summer\'s day?\n'
generated_text = start_text.lower().split()
for i in range(100):
    input_seq = embedding_model(generated_text).numpy().reshape(1, seq_length, 300)
    prediction = model.predict(input_seq).reshape(300)
    generated_text.append(embedding_model.get_nearest_neighbors(prediction)[0])

generated_text = ' '.join(generated_text)
generated_text = generated_text.replace(' ,', ',').replace(' .', '.').replace(' !', '!').replace(' ?', '?').replace(' ;', ';')
print(generated_text)