---
aliases: 
tags: study, reinforcement-learning
---

## Model-Free Control
- model-free prediction을 통해 주어진 정책을 따라 에이전트가 움직이게 한 다음, 그 경험으로부터 각 상태의 가치를 학습 가능.
- 최고의 정책을 찾는 방법은?
- model-free에서는 액션 선택 확률 분포나 상태 전이 확률 분포를 알 수 없기 때문에 각 상태의 가치 업데이트, 정책 업데이트(그리디 등)가 불가능하다.
- 해결책으로는,
	- 각 상태의 밸류 계산(prediction)에 MC 혹은 TD를 사용
	- $q(s, a)$를 사용하여 액션 결정 ($v(s)$만으로는 전이 확률을 알 수 없으므로)
		- 이 또한 MC 기법으로 구한다. 예전('모두를 위한...')에 배웠던 **decaying $\epsilon$ greedy**
		- 정책 평가 단계에서는 MC를 이용하여 q를 구하고, 정책 업데이트시 e-greedy 적용.
		- 한번 업데이트가 되면 계속 그 길로만(exploit) 갈 것이기 때문

### Monte-Carlo Control
- 수렴할 때 까지 n번 반복;
	- 한 에피소드(도착지까지)의 경험을 쌓고
	- 경험한 데이터로 $q(s, a)$ 테이블의 값을 업데이트 하고 (정책 평가)
	- 업데이트 된 $q(s,a)$ 테이블을 이용하여 e-greedy 정책 업데이트 수행

### SARSA
- 정책 평가를 TD 방식으로 변경.
- $S \xrightarrow A_{+R} S' \xrightarrow A'$
- 

