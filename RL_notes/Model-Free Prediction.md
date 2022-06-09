---
aliases: planning, 플래닝
tags: study, reinforcement-learning
---

## Planning
### Planning by Dynamic Programming
- 복잡한 문제를 subproblems로 디컴포즈 하여 푸는 방법론
- **optimal substructure**가 필요, **overlapping subproblems**여야 함.
	- 하부 구조가 있어야 하고, 캐싱 가능한 결과들을 내야 함

### 반복적 정책 평가, "그리드 월드" 예시
- "그리드 월드"
	- 정책 함수 $\pi$는 "4방향 각각 0.25 확률"로 정의 가능
	- 보상 함수 $r^a_s$는 어느 액션을 하든 -1로 고정
	- 전이 확률 $P^a_{ss'}$은 가장자리의 $s$들을 제외하면 100% (즉, 선택한 액션대로 전이)
- 4 x 4테이블을 모두 0.0으로 초기화
- 마지막 칸의 경우, $v(s)$는 '미래에 받게 될 누적 보상'이므로, 미래가 없으니 0.0으로 남게 된다.
	- 즉, 업데이트를 하지 않고 0으로 남아있는 것.
- 책(p87~88)에서 모든 $s$에 대해 반복한다고 하는데, 이미 업데이트 된 $s$의 값을 쓰지 않고 다 0.0인 것으로 돌게 되면 안되는것 아닌가? 테이블 방식의 업데이트는 원래 그렇게 하는건가?
	- 그리고, 가장자리에서는 갈 수 없는 곳이 있으므로 무작정 계산하게 되면 안될 것 같고 선택지에서 빼는건가? 그렇게 설명이 되어있지 않던데.
	- 현재 $S$에 대해서만 평가를 하고 다음 $S'$로 넘어가는것.

## Model-Free : Evaluating without MDP
- MDP를 모르는 상황에서의 prediction. 즉, $\pi$가 주어졌을 때 가치를 평가하는 두 가지 방법
	- **monte-carlo learning**
	- **temporal-difference learning**
- 그리드월드 같은 작은 MDP에서는 여전히 table look-up방법론을 사용한다.

### Monte-Carlo Learning
- 확률이 알려지지 않은 동전 혹은 주사위를 던질 때의 **기대값**을 구하는 것과 같다.
	- 즉, 확률에서 기대값을 구하는 것이 아니라 여러 번 던져본 결과를 기대값으로 결론짓는 것.
- 가치 함수의 정의는 리턴의 기대값
$$ v_\pi(s_t) = \mathbb{E}_t[G_t] $$
- ex) 동전을 10번 던져서 앞면이 나오면 가진다. : 10번 던지는 행위가 1 에피소드
- **대수의 법칙 (Law of large numbers)** : 커질 수록 정확도가 올라간다
- 그리드월드의 $s_0$에서 출발하여 $s_T$에 도착하는 과정
$$ s_0, a_0, r_0, s_1, a_1, r_1, s_2, a_2, r_2, \dots, s_{T-1}, a_{T-1}, r_{T-1}, s_T $$
- 각 상태에 대한 리턴 $G$는 아래와 같이 정의 가능
$$
\begin{aligned}
G_0 &= r_0 + \gamma r_1 + \gamma^2 r_2 + \dots + \gamma^{T-1} r_{T-1}\\
G_1 &= r_1 + \gamma r_2 + \gamma^2 r_3 + \dots + \gamma^{T-2} r_{T-1}\\
G_n &= r_n + \gamma G_{n+1}\\
\vdots\\
G_{T-1} &= r_1\\
G_{T} &= 0
\end{aligned}
$$
- 여기서 $\gamma$와 보상 $r_0, \dots, r_{T-1}$은 모두 관측된 숫자 값으로, 변수가 아님. 따라서 리턴들도 모두 숫자 값.
- 각 $s$에 대해, time-step $t$의 방문 수를 $N(s)$라 하고 밸류를 $V(s)$라 하면 아래와 같이 업데이트가 가능하다.
$$
\begin{aligned}
N(s) &\leftarrow N(s) + 1\\
V(s) &\leftarrow V(s) + G_t\\
\end{aligned}
$$
- 목적지 도착까지를 1 에피소드라 하고, 충분한 수의 에피소드를 실행한 후의 최종 밸류 $v_\pi$는 평균값을 구하면 된다.
$$
v_\pi \approxeq \frac{V(s)}{N(s)}
$$
- 모든 에피소드를 다 마치고 하는 것이 아니라 매 에피소드마다 업데이트 하는 방법 : 리턴값은 평균이고, 평균은 아래와 같이 incremental하게 계산할 수 있다.
$$
\begin{aligned}
\mu_k &= \frac{1}{k} \sum^k_{j=1} x_j\\
&= \frac{1}{k} \left(x_k + \sum^{k-1}_{j=1} x_j \right)\\
&= \frac{1}{k} (x_k + (k - 1) \mu_{k-1})\\
&= \mu_{k-1} + \frac{1}{k}(x_k - \mu_{k-1})
\end{aligned}
$$
- 따라서 이전의 $N(s_t)$와 $V(s_t)$를 revisit하면,
$$
\begin{aligned}
N(s_t) &\leftarrow N(s_t) + 1\\
V(s_t) &\leftarrow V(s_t) + \frac{1}{N(S_t)} (G_t - V(S_t)) \\
\end{aligned}
$$
- 학습률  $\alpha$를 도입하는 방법과 비교
$$
\begin{aligned}
V(s_t) &\leftarrow (1-\alpha) \times V(s_t) + \alpha \times G_t\\
V(s_t) &\leftarrow V(s_t) + \alpha \times (G_t - V(s_t))
\end{aligned}
$$

### Temporal Difference Learning
- MC는 업데이트 하려면 에피소드가 끝나야 한다. 종료 조건이 없는 경우는?
- 종료하지 않는 MDP에서는 리턴이 존재하지 않는데 어떻게 학습을 할까?
	- 추측을 추측으로 업데이트 하자. Update a guess towards a guess
		- 더 정확히는, 미래의 추측으로 과거의 추측을 업데이트
	- 날씨의 예시
		- MC : 일요일에 비가 오는 것을 보고 금요일의 강우 확률을 업데이트
		- TD : 토요일의 강우 확률을 보고 금요일의 값을 업데이트
- 다시 MC로 돌아가서, 가치 함수 $v_\pi(s_t)$의 정의는 리턴 $G_t$(에피소드 종료 후 얻게 되는)의 기대값.
	- $v_\pi(s_t) = \mathbb{E}_\pi[G_t]$
	- 따라서 $G_t$를 많이 모으면(수행을 여러 번 하여) 가치함수에 수렴시킬 수 있다.
	- 통계학 용어로는, ==$G_t$는 $v_\pi(s_t)$의 unbiased estimate== 라 한다.
- TD의 경우, $G_t$대신 $r_{t+1} + \gamma V(s_{t+1})$를 사용.
	- **TD 타겟 target** : $r_{t+1} + \gamma V(s_{t+1})$
	- **TD 오차 error ($\delta_t$)** : $r_{t+1} + \gamma V(s_{t+1}) - V(s_t)$ 

$$
\begin{aligned}
\text{MC : } V(s_t) &\leftarrow V(s_t) + \alpha \times (G_t - V(s_t))\\
\text{TD : } V(s_t) &\leftarrow V(s_t) + \alpha \times (r_{t+1} + \gamma V_\pi(s_{t+1}) - V(s_t))\\
V(s_t) &\leftarrow V(s_t) + \alpha \delta_t
\end{aligned}
$$
- TD와 MC의 차이점은 **업데이트 수식** 과, **업데이트 시점** 뿐.
$$
s_0 \rightarrow 
s_1 \rightarrow 
s_2 \rightarrow 
s_3 \rightarrow 
s_7 \rightarrow 
s_6 \rightarrow 
s_{10} \rightarrow 
s_{11} \rightarrow 
s_{15} \text{(END)}
$$
$$
\begin{aligned}
V(s_0) &\leftarrow V(s_0) + 0.01 \times (-1 + V(s_1) - V(s_0))\\
V(s_1) &\leftarrow V(s_1) + 0.01 \times (-1 + V(s_2) - V(s_1))\\
\vdots\\
V(s_{15}) &\leftarrow V(s_{11}) + 0.01 \times (-1 + V(s_{15} - V(s_{11}))\\
\end{aligned}
$$
### MC vs. TD
- non-episodic MDP에서는 TD만 가능하다.
	- Episodic : 종료 상태가 있어서 경험이 에피소드 단위로 쌓이는 MDP. 바둑, 게임 등
	- Non-episodic : 종료 상태가 없거나 한 에피소드가 무한에 가깝게 길 경우. 주식 시장 등
- MC는 실제 리턴을 계산해서 구하기 때문에 편향되지 않지만, TD는 편향성을 가진다.
	- $v_\pi$는 정책 $\pi$의 실제 가치이며, MC가 아니면 알 수 없다.
	- $V$는 업데이트 중인 테이블에 적혀 있는, $v_\pi$와 같아지길 바라는 값이다.
	- 즉, TD에서는 샘플을 무한히 모아도 실제 가치에 가까워진다는 **보장은 없다.**
		- 하지만 잘 작동한다.
- MC는 분산이 매우 크고, TD는 작다.
	- MC는 전체 과정을 다 거친 결과에서 도출되고, TD는 세부 과정마다 조정을 거치기 때문
	- 분산이 크다는 것은 샘플 데이터가 많이 필요하다는 의미이므로 제한된 샘플에서는 TD가 더 유리

### MC + TD ?
- 더 실용적인 선택지에 대한 고민.
	- 사실, MC는 TD의 한 극단이다. ==n-step TD==의 개념
- TD target : $r_{t+1} + \gamma V(s_{t+1})$
	- 1 스텝에 대한 결과지만, 스텝을 더 확장할 수 있다. 만약 종료 시점의 스텝을 $T$라 하면 그냥 리턴이 되는 것.

$$
\begin{aligned}
&r_{t+1} + \gamma V(s_{t+1})\\
&r_{t+1} + \gamma V(s_{t+1}) + \gamma^2 V(s_{t+2})\\
&r_{t+1} + \gamma V(s_{t+1}) + \gamma^2 V(s_{t+2}) + \gamma^3 V(s_{t+3})\\
&\vdots\\
&r_{t+1} + \gamma V(s_{t+1}) + \gamma^2 V(s_{t+2}) + \gamma^3 V(s_{t+3}) + \dots + \gamma^{T-1} R_T
\end{aligned}
$$
- 1 스텝 단위의 업데이트를 TD(0)이라고 표기한다. 즉, MC vs. TD(0)인 것.
	- n 스텝의 경우는 TD(n-1)이고, 적절한 n은 정답이 없다.
		- 아타리 게임 연구에서는 n을 5로 뒀음.
		- https://jay.tech.blog/2017/01/19/asynchronous-advantage-actor-critic-a3c/

