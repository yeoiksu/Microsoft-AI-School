# Day34. Townhall Meeting II. Tokenizer & Transformer
## I. Tokenizer
### Tokenizer란 ?
- 입력된 텍스트를 인공지능 모델이 처리할 수 있는 데이터(숫자)로 변환하는 과정

### 1. 단어 기반 토큰화(Word-based Tokenization)
- 단어 단위로 토큰화
- unknown 토큰을 많이 생성

### 2. 문자 기반 토큰화(Character-based Tokenization)
- 문자를 기반으로 토큰화
- unknown 토큰이 훨씬 적어짐

### 3. 하위 단어 토큰화(Subword Tokenization)
- 문자기반, 단어기반 방식의 장점을 최대한 활용하기 위해 결합된 방식
- 빈번하게 사용되는 단어는 분할 X
- 희귀한 단어는 하위단어로 분할 O

### 4. 세부적인 기법들
- Byte-leve BPE (GPT-2에 사용됨)
- WordPiece (BERT에 사용됨)
- SentencePiece, Unigram (몇몇 다국어 모델에 사용됨)
<hr>

## II. Transfomer
### 1. Seq2seq
- encoder가 문맥을 고려한 sequence를 받아 context vector를 만들고 이
context vector로 decoder에서 sequence를 만드는, 다음 state를 예측하는 기법
- 단점:
    [1] 길면 처음 정보가 미미해진다. 단점을 보안하기위해 <strong>"attention"</strong> 기법사용
    [2] Fixed size context vector로 긴 문장의 정보를 압축하기 떄문에 잘 압축 X
    [3] 모든 token이 영향을 미치는 것 때문에 중요하지 않은 toekn의 영향을 받음

#### Attention Mechanism 
- 디코더에서 출력 단어를 예측하는 매 시점(time step)마다, 인코
더에서의 전체 입력 문장을 다시 한 번 참고한다는 것
- 단, 전체 입력 문장을 전부 다 동일한 비율로 참고하는 것이 아니라, 해당 시점에서 예측해야할 단어와 연관이 있는 입력 단어 부분을 좀 더 집중(attention)
- Attention Mechanism에서 필요한 3가지 paramater
    [1] Query (Q) = t 시점의 디코더 셀에서의 은닉 상태
    [2] Keys  (K) = 모든 시점의 인코더 셀의 은닉 상태들
    [3] Values(V) = 모든 시점의 인코더 셀의 은닉 상태들

### 3가지 종류 언어모델
- 언어에 대한 통계적 이해를 가진 모델

#### 1. Decoder-only 모델 Auto regressive model (GPT1, GPT2, GPT3, ..
- few shot learning 사용
- 단점: 모델이 너무 큼
- 점점 더 모델이 커지고있음(모델이 크고, 데이터를 많이 넣을수록 성능이 좋다.)

#### 2. Encoder-only 모델 Auto encoder (BERT, RoBERTa, Electra, Albert, ..
- input을 vector 로 바꿔준다.
- vector는 의미와 관련이 있다. 
- Pre-training(사전학습, 비지도학습) >> fine-tuning(지도학습)
- Downstream task(번역, 문장 분류, 질의응답, ...)
- Why? 
    1. 성능이 기존 방식보다 훨씬 좋다
    2. 소량의 데이터로도 학습이 훨씬 빨리된다

#### 3. Encoder-Decoder 모델 >> Transformer 모델과 구조는 동일(BART, T5)

   - Pre-training(사전학습, 비지도학습) >> fine-tuning(지도학습)
   - 생성 관련 Task 사용
