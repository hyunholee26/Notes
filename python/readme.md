- iterable: 객체 안에 있는 원소를 하나씩 반환 가능한 객체
- iterator: iter()라는 함수가 반환하는 객체, next()를 통해 호출가능, 순차적으로 호출
- iterable 객체 A -> iter(A) -> Iterator 객체 B -> next(B) -> element(data)

Question? 우리는 list 같은 이터러블(Iterable) 객체와 for 문을 쓰면서 한번도 iter() 나 next()를 보지 못했는뎁쇼????
파이썬의 for 문은 이터러블(Iterable) 객체를 만나, 내부적으로 iter() 함수를 호출하여, 이터레이터(Iterator)를 생성합니다. 이 생성된 이터레이터(Iterator)가 루프가 실행되면서 next() 를 호출하며 반복적인 데이터를 뽑아 낼 수 있게 되는 것입니다. 그리고 모든 원소가 뽑아지고 난 뒤에는 StopIteration 이 발생하며, for 문이 종료 됩니다.

```
for element in iterable_object:
    print(element)
```
=>
```
# iter() 함수를 호출해, iterator 를 생성하고, 
iterator_object = iter(iterable_object)

while True:
    # next() 함수를 호출해, element 를 받아옵니다.
    try:
        element = next(iterator_object)
        print(element)

    # element 가 없을 시, StopIteration Exception 발생
    except: StopIteration:
        break
```

enumerate() 함수는 인자로 넘어온 목록을 기준으로 인덱스와 원소를 차례대로 접근하게 해주는 반복자(iterator) 객체를 반환해주는 함수입니다. 이 부분은 enumerate() 함수의 반환 값을 리스트로 변환해보면 좀 더 명확하게 확인할 수 있습니다.
```
>>> list(enumerate(['A', 'B', 'C']))
[(0, 'A'), (1, 'B'), (2, 'C')]
```

----

Dataset
머신러닝, 딥러닝 학습에 사용되는 방대한 데이터의 크기 때문에 데이터를 한 번에 불러오기 쉽지 않습니다. 따라서 데이터를 한 번에 부르지 않고 하나씩만 불러서 쓰는 방식을 택해야 합니다. 모든 데이터를 불러놓고 사용하는 기존의 Dataset 말고 Custom Dataset 이 필요합니다.

Dataset class는 전체 dataset을 구성하는 단계입니다. input으로는 지도학습에 일반적인 x(input feature)과 y(label)을 tensor로 넣어주면 됩니다. PyTorch의 TensorDataset은 tensor를 감싸는 Dataset입니다.

Dataset Class에서 반드시 정의해야 하는 Method 들은 다음과 와 같습니다.

 - init(self): 여기서 필요한 변수들을 선언한다. init 함수는 Dataset 객체가 생성될 때 한 번만 실행됩니다.
 - get_item(self, index): 만든 리스트의 index 에 해당하는 샘플을 데이터셋에서 불러오고 전처리를 실행한 다음 tensor 자료형으로 바꾸어 리턴하는 구조이다.
 - len(self): 학습 데이터의 갯수를 리턴한다.

```
class CustomDataset(Dataset):
    def __init__(self):
    # 생성자, 데이터를 전처리 하는 부분   

    def __len__(self):
    # 데이터셋의 총 길이를 반환하는 부분   

    def __getitem__(self,idx):
    # idx(인덱스)에 해당하는 입출력 데이터를 반환한다.
```

선형 회귀를 위해 Dataset을 만든다면 다음과 같은 코드가 될것입니다.

```
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self):
        self.x_data = [[73, 80, 75],
                            [93, 99, 93]]
      self.y_data = [[152], [185]]

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):
        x = torch.FloatTensor(self.x_data[idx])
      y = torch.FloatTensor(self.y_data[idx])

      return x, y

dataset = CustomDataset()
```
DataSet은 DataLoader를 통하여 data를 받아오는 역할을 합니다.

---
DataLoader
DataLoader는 PyTorch 데이터 로딩 유틸리티의 핵심입니다. DataLoader의 가장 중요한 인자는 데이터를 불러올 데이터셋 객체를 나타내는 데이터셋입니다. 모든 Dataset 으로부터 DataLoader 를 생성할 수 있습니다. PyTorch의 DataLoader 는 배치 관리를 담당합니다. DataLoader란 Dataset을 batch기반의 딥러닝모델 학습을 위해서 미니배치 형태로 만들어서 우리가 실제로 학습할 때 이용할 수 있게 형태를 만들어주는 기능을 합니다. DataLoader를 통해 Dataset의 전체 데이터가 batch size로 slice되어 공급됩니다. 앞서 만들었던 dataset을 input으로 넣어주면 여러 옵션(데이터 묶기, 섞기, 알아서 병렬처리)을 통해 batch를 만들어줍니다. DataLoader는 iterator 형식으로 데이터에 접근 하도록 하며 batch_size나 shuffle 유무를 설정할 수 있다.

일반적인 사용 방법은 다음과 같다.

```
from torch.utils.data import Dataloader

dataloader = Dataloader(
      dataset,
    batch_size = 2,
    shuffle = True,
)
```

DataLoader의 정의는 다음과 같습니다.

```
DataLoader(dataset, batch_size=1, shuffle=False, sampler=None,
           batch_sampler=None, num_workers=0, collate_fn=None,
           pin_memory=False, drop_last=False, timeout=0,
           worker_init_fn=None)
```

 - batch_size 는 각 minibatch의 크기 즉 한 번의 배치 안에 있는 샘플 사이즈를 말합니다. 통상적으로 2의 제곱수로 설정합니다 (예: 16, 32, 64...) 데이터셋의 크기가 그렇게 크지 않으면 굳이 사용하지 않아도 되지만, 데이터셋의 크기가 매우 큰 경우엔 모든 데이터를 한 번에 넣어서 처리하는 방식을 적용하기엔 무리가 있습니다. 그래서 Mini Batch 라는 개념으로 (묶음) 한 번에 한 묶음씩 처리하는 방식을 사용하게 됩니다. 정리하면, 전체 데이터셋을 batch size 크기로 묶어서 iteration의 수 만큼 실행하는 것입니다.

 - shuffle 은 Epoch 마다 데이터셋을 섞어, 데이터가 학습되는 순서를 바꾸는 기능을 말합니다. 학습할 때는 항상 True로 설정하는 것을 권장합니다.

 - num_worker는 동시에 처리하는 프로세서의 수입니다. 서버에서 돌릴 때는 num_worker를 조절해서 load속도를 올릴 수 있지만, PC에서는 default=0로 설정해야 오류가 안납니다. num_worker 하나를 더 추가 하면 20% 정도 속도가 빨라 진다고 합니다. 그러나 무작정 num_worker 수를 늘린다고 속도가 빨라지는 것은 아닙니다. 공급되는 배치를 처리하는 빠른 프로세서가 있어야 속도가 빨라지므로 적절한 조절이 필요합니다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FRTEmw%2Fbtrg7W94B87%2FeGpxZW4aD5Cix28s6TYw8K%2Fimg.png)

