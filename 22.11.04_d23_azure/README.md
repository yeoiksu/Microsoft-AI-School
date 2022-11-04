# Day23. ML.

## 1. Azure Machine Learning 사용하기
### 1.1. "Azure Machine Learning" 생성 & Dataset 설정
    [1]  + 리소스 만들기
    [2] 'Azure Machine Learning' 만들기 선택
    [3] <기본> 이름, 지역 설정
    [4] 검토 + 만들기
    [5] 생성 이후 리소스로 이동
    [6] 아래의 'Studio 시작하기' 클릭
    [7] 왼쪽 tab의 'Compute'에서 사용 가능한 core확인 후 생성
    [8] 왼쪽 tab의 'Data' >> create >> 폴더 안의 'titanic_train.csv' upload >> CREATE
    -> 3가지 기능 선택 가능 Notebook(자주 사용), Automated ML, Designer(Orange3와 비슷)

### 1.2. Automated ML 사용하기
    [1] 왼쪽 tab의 'Automated ML' >> '+ New Automated ML job'
    >> Select data asset
    [2] Dataset 다시 create (아까와 다름) >> 폴더 안의 'titanic_train.csv' upload >> next
    [3] 'Schema' 옵션에서 필요없는 Column name을 제외 할 수 있다. (Survive, Pclass, Sex, Age만 살림) >> CREATE >> 'Refresh'하면 dataset 생성 확인 가능
    [4] Titanic Dataset 선택 후 NEXT
    >> Configure Job
    [5] 'Name(사용자 설정), Target column(Survived), Select compute type(Compute instance)' >> NEXT
    >> Select task and settings
    [6] Classification (Enable Deep Learning하면 시간이 더걸림)
    >> Select the validation and test type
    [7] 기본을 skip >> FINISH

    >> Evaluate Model
    [8] 위쪽 tab의 'Models'를 확인하면 다양한 classification model과 'AUC weighted'을 통해 성능 확인
    [9] model을 선택하여 'Download'하면 yaml, pkl 파일을 다운로드 가능
### 1.3. Notebook 사용하기    
    [1] Notebook에서 작성한 내용을 바탕으로 왼쪽 tab의 'Job'에서 새로운 diabetes_experiment가 생성된 것을 확인 가능
    [2] Folder에서 output에서 model이 생성된 것 확인가능
    [3] 왼쪽 tab의 Jobs >> 해당 experiment >> model의 성능 확인 가능 