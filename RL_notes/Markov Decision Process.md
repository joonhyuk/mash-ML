---
aliases: MDP, 마르코프
tag: study, reinforcement-learning
---
## 마르코프 결정 프로세스
[Lectures](https://www.davidsilver.uk/teaching/) from [David Silver](https://davidsilver.uk)
"바닥부터 배우는 강화학습" - 노승은 저

- 강화 학습은 순차적 의사 결정 문제를 푸는 방법론
- 순차적 의사결정 문제는 Markov Decision Process (MDP)라는 개념을 통해 더 정확하게 **표현** 가능
    - Markov Process → Markov Reward Process → Markov Decision Process

### Markov Process
$$ \text{MP} \equiv (S, P) $$
- 상태의 집합 $S$
    - $S = \{s_0, s_1, s_2, ...\}$
- 전이 확률(transition probability) $P_{ss'}$
    - $P_{ss'} = \mathbb{P} [S_{t+1} = s' | S_t = s]$
        - 조건부 확률 : bar의 오른쪽에 주어진 조건을 기술
    - `len(S) ^ 2`의 행렬로 표현 가능. FSM 이구만.
- 마르코프 성질(Markov property)
    - **"미래는 오로지 현재에 의해 결정된다."**
        - (외부 요인 역시 현재를 이루는 요소라고 보면 될 듯)
    - $\mathbb{P}[S_{t+1}|S_t] = \mathbb{P}[S_{t+1}|S_1, S_2, ..., S_t]$
    - ==의문점== : 맞는 말이긴 한데 대부분의 엔트로피 상황에서 현재는 과거에 의해 다양하게 나올 수 있다. 같은 상황(값들로 정의 가능한)에서 다음 상황으로의 전이 확률은 이전의 상태들에 의해 영향을 받게 된다. 대표적으로는 인간이 하는 도박들.
	    - 즉, 확률이 고정될 수 없다...임. 아이가 잠에 드는 상황을 예로 들면, 누워있다가 일어나는 확률은 초기에 높다가 갈수록 줄어들 것이다.
	    -  ==나름의 해답== : 모든 것이 '상태'에 다 들어가 있으면 말이 된다. 즉, 아이가 잠에 드는 상황의 경우 책에서 처럼 단순한 행렬로는 표현할 수 없다. $s_0 \rightarrow s_1 \rightarrow s_0$의 반복 수 마다 $s_0$이 다르게 정의된다.
- 마르코프 하지 않은 상태
	- 예를 들면 운전중의 상태의 순간 스냅샷 한 장뿐인 경우, 마르코프하지 않다고 할 수 있다.
		- 최근 10초의 스냅샷 10장을 상태에 포함시키면 조금 더 마르코프하다고 볼 수 있다. 또는 속도 벡터, 가속도 벡터, 목적지, 주변 차량의 정보 등이 있으면 점점 더 마르코프 해진다.

### Markov Reward Process
$$ \text{MRP} \equiv (S, P, R, \gamma) $$
- Markov Process에 보상의 개념이 추가된 결과물
- 보상 함수 $R$
	- 어떤 상태 $s$에 도착했을 때 받게 되는 보상
	- $R_s = \mathbb{E}[R_{t+1}|S_t =s]$ ($\mathbb{E}$ : 기대값)
- 감쇠 인자 $\gamma$
	- $\gamma \in [0, 1]$. 미래 보상의 반영율

#### State Value Function
- 상태 $s$로 부터 시작하여 얻는 리턴$G$의 기대값
$$ v(s) = \mathbb{E}[G_t|S_t = s] $$
-  $G$ = '리턴' : 현재부터 미래에 얻게 될 보상의 합
	- 강화 학습은 '보상'이 아니라 '리턴'을 최대화 하도록 학습하는 것
	- $\gamma$가 작을 수록 현재에 집중하는 greedy한 에이전트가 된다.

#### Bellman Equation for MRPs
- value function은 두 부분으로 나눠진다.
	- 즉시 받는 리워드 $R_{t+1}$ 
	- 감쇠된 향후 리워드 총합 $\gamma v(S_{t+1})$

$$
\begin{aligned}
v(s) &= \mathbb{E} [G_t|S_t=s]\\
&= \mathbb{E} [R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ... |S_t = s]\\
&= \mathbb{E} [R_{t+1} + \gamma (R_{t+2} + \gamma R_{t+3} + ...) |S_t = s]\\
&= \mathbb{E} [R_{t+1} + \gamma G_{t+1} |S_t = s]\\
&= \mathbb{E} [R_{t+1} + \gamma v(S_{t+1}) |S_t = s]\\
\\
v(s) &= R_s + \gamma \sum_{s' \in S} P_{ss'}v(s')\\
\\
v &= R + \gamma Pv\\
\begin{bmatrix}v(1)\\ \vdots \\v(n)\end{bmatrix} & = \begin{bmatrix}R_1\\ \vdots \\R_n\end{bmatrix} + \gamma \begin{bmatrix}P_{11} \dots P_{1n}\\ \vdots \\P_{n1} \dots P_{nn}\end{bmatrix}\begin{bmatrix}v(1)\\ \vdots \\v(n)\end{bmatrix}
\end{aligned}
$$
- 선형 식이므로 $v$로 정리
$$ v = \frac{R}{1 - \gamma P} $$


### Markov Decision Process
$$\text{MDP} \equiv (S, A, P, R, \gamma)$$
- 액션의 집합 $A$
- 전이 확률 행렬 $P^a_{ss'}$
	- 현재 상태 $s$에서 액션 $a$를 선택했을 때 다음 상태가 $s'$가 될 확률
	- $P^a_{ss'} = \mathbb{P}[S_{t+1} = s'|S_t = s, A_t = a]$
	- $s'$가 결정되어 있지 않음에 주의. 액션 실행 후 도달하게 될 상태 $s'$에 대한 확률 분포 행렬임
- 보상 함수 $R^a_s$
	- 현재 상태 $s$에서 액션 $a$를 선택했을 때 받는 보상
	- $R^a_s = \mathbb{E}[R_{t+1}|S_t = s, A_t = a]$

#### Policy Function
- 각 상태에서 어떤 액션을 선택할지 정해주는 함수
	- 리턴을 최대화 하는 결정
- 상태 $s$에서 액션 $a$를 선택할 **확률**로 정의된다.
$$
\pi(a|s) = \mathbb{P}[A_t = a|S_t = s]
$$
- 정책은 stationary(time-independent) 하다
$$
A_t \sim \pi(\cdot|S_t), \forall t > 0
$$
- 어떤 MDP $M = (S, A, P, R, \gamma)$가 있고, 정책이 $\pi$라 하면, (제대로 이해하지 못함 #todo ) 
	- 상태 시퀀스 $S_1, S_2, \dots$는 Markov Process $(S, P^\pi)$
	- 상태와 보상의 시퀀스 $S_1, R_2, S_2, \dots$는 Markov Reward Process $(S, P^\pi, R^\pi, \gamma)$가 된다
	- where,

$$
\begin{aligned}
P^\pi_{s, s'} &= \sum_{a \in A} \pi (a|s) P^a_{ss'}\\
R^\pi_s &= \sum_{a \in A} \pi (a|s) R^a_s
\end{aligned}
$$
#### State Value Function
- $s$부터 끝까지 $\pi$를 따라서 행동할 때 얻게되는 리턴의 기대값
	- MRP의 경우와 같지만, $\pi$에 의존적이 된다.

$$
\begin{aligned}
v_\pi(s) &= \mathbb{E}_\pi[r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + \dots |S_t = s]\\
&= \mathbb{E}_\pi[G_t|S_t = s]
\end{aligned}
$$

#### Action Value Function
- state value function이 어떤 상태가 주어졌을 때 그 상태를 평가하는 함수라면, 각 상태에서의 액션도 평가할 필요가 있다.
- 정확히는 state-action value function임
	- 상태에 따라 액션의 가치가 달라지기 때문
- 즉, $s$에서 $a$를 선택하고, 그 이후에는 $\pi$를 따라서 행동할 때 얻게되는 리턴의 기대값

$$
\begin{aligned}
q_\pi (s, a) = \mathbb{E}_\pi [G_t|S_t = s, A_t = a]
\end{aligned}
$$
- 따라서 $v_\pi(s)$와 $q_\pi(s, a)$는 **$s$에서 어떤 액션을 선택하는가**의 차이만 있음
	- $v_\pi(s)$를 계산할 때는 $s$에서 $\pi$가 액션을 선택하지만, $q_\pi(s, a)$에서는 $s$에서 '강제로'(?) $a$를 선택하는 상황. ==즉, $q_\pi(s, a) = \mathbb{E}[R_t|S_t = s, A_t = a] + v_\pi(s_{t+1})$ 라고 봐도 될지?== #todo 

#### Bellman Expectation Equation
- [[Bellman Equation#Bellman Expectation Equation]]

#### Optimal Value Functions
- [[Bellman Equation#Bellman Optimal Equation]]

### Prediction & Control
- 주어진 상황이 있을 때 이를 MDP의 형태로 만들어야 풀 수 있다.
	- MDP를 푼다는 것은, prediction과 control의 태스크를 수행하는 것.
- **Prediction** : $\pi$가 주어졌을 때, 각 상태의 밸류를 평가하는 문제
- **Control** : optimal policy $\pi^*$를 찾는 문제