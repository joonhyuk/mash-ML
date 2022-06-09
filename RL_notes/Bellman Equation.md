---
aliases: 벨만 방정식
tag: study, reinforcement-learning
---
## Bellman Equation
### Bellman Expectation Equation
$$
\begin{aligned}
v_\pi (s_t) &= \mathbb{E}_\pi [r_{t+1} + \gamma v_\pi(s_{t+1})]\\
q_\pi (s_t, a_t)&= \mathbb{E}_\pi [r_{t+1} + \gamma q_\pi(s_{t+1}, a_{t+1})]\\
\\
\\
v_\pi (s) &= \sum_{a \in A} \pi(a|s) q_\pi(s,a)\\
q_\pi (s, a)&= r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_\pi(s')\\
\\
\\
v_\pi (s) &= \sum_{a \in A} \pi(a|s) \left( r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_\pi(s') \right)\\
q_\pi (s, a)&= r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} \sum_{a' \in A} \pi(a'|s') q_\pi(s',a')\\
\end{aligned}
$$
- $s_t$에서 시작하여 $s_{t+1}$이 정해지기 까지는 두 번의 확률적인 과정을 거친다.
	- 정책이 액션의 확률 분포에 의해 액션을 결정
	- 액션이 선택되고 나면 환경의 전이 확률 분포에 의해 다음 상태가 결정
	- 즉, 상태 $s_t$에서 액션 $a_t$를 선택한 후, 다음 상태 $s_{t+1}$가 어디가 될 지는 전이 확률 $P^{a_t}_{s_t s_{t+1}}$에 의해 결정
- $v_\pi (s) = \sum_{a \in A} \pi(a|s) q_\pi(s,a)$
	- $s$에서의 밸류 $v_\pi (s)$는,
	- 모든 $a$에 대해,
	- $s$에서 $a$를 실행할 확률 $\pi(a|s)$을, 
	- $s$에서 $a$를 실행하는 것의 밸류 $q_\pi(s,a)$에 곱한 **기대값의 총합**이다.
- $q_\pi (s, a) = r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_\pi(s')$
	- $s$에서 $a$를 실행하는 것의 밸류 $q_\pi(s,a)$는,
	- 일단 $s$에서 $a$를 선택하면 받는 보상 $r^a_s$을 받고,
	- 도착 가능한 모든 $s'$에 대해,
	- $s$에서 $a$를 실행하면 $s'$에 도착할 확률 $P^a_{ss'}$을, 
	- 도착지 $s'$의 밸류 $v_\pi(s')$에 곱한 **기대값의 총합**에 감쇠율을 곱한 값이다.
- 결국, 기대값 구하는 공식이 완성되었다
	- 현재의 밸류와 다음 밸류의 연결 고리

$$
\begin{aligned}
v_\pi (s_t) &= \mathbb{E}_\pi [r_{t+1} + \gamma v_\pi(s_{t+1})]\\
v_\pi (s) &= \sum_{a \in A} \pi(a|s) \left( r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_\pi(s') \right)
\end{aligned}
$$
- 최종 식을 계산하기 위해서는 다음 2가지를 반드시 알아야 한다
	- **보상 함수 $r^a_s$** : 각 상태에서 액션을 선택하면 얻는 보상
	- **전이 확률 $P^a_{ss'}$** : 각 상태에서 액션을 선택하면 다음 상태가 어디가 될 지에 대한 확률 분포
	- ==액션 선택을 위한 확률 분포는?==
	- 보상 함수와 전이 확률은 주어지는 환경의 일부. 이들을 알게 되면 "MDP를 안다"라고 할 수 있다.
- 실제 세계에서는 모든 정보를 가지고 있는 경우가 드물다.
	- **model-free approach** : MDP에 대한 정보를 모르고 접근하여 경험으로 학습
	- **model-based approach** : 정보를 다 알고 시뮬레이션. **planning**이라고도 한다.

### Bellman Optimal Equation
- $v_\pi(s), q_\pi(s, a)$는 정책이 $\pi$로 고정되어 있을 때의 밸류에 대한 함수.
- 반면, $v_*(s), q_*(s, a)$는 optimal value에 대한 함수.

$$
\begin{aligned}
v_*(s) &= \max_\pi v_\pi(s)\\
q_*(s,a) &= \max_\pi q_\pi(s,a)
\end{aligned}
$$
- 어떤 MDP가 주어졌을 때, 그 MDP 안에 존재하는 모든 $\pi$들 중에서 가장 좋은 ($v_\pi(s)$를 최대로 만들어주는)$\pi$를 선택하여 계산한 밸류가 optimal value $v_*(s)$이다. 아래의 상황에서 $\pi_1$이 '더 좋은 ' 정책이다.
$$
\forall s \in S, v_{\pi_1}(s) > v_{\pi_2}(s) \rightarrow \pi_1 > \pi_2
$$
- 정책 $\pi$의 수가 무한대일 때, 모든 $s$에 대해 최적 밸류를 내게 해 주는 정책 $\pi_*$가 최소한 1개 이상 존재한다는 것을 증명 가능하다. #todo 
	- 즉, **MDP 내의 모든 $\pi$에 대해, $\pi_* > \pi$ 를 만족하는 $\pi_*$가 반드시 존재한다.

$$
\begin{aligned}
v_*(s) &= \max_a \mathbb{E}[r + \gamma v_*(s')|s_t=s, a_t=a]\\
v_*(s_t) &= \max_a \mathbb{E}[r_{t+1} + \gamma v_*(s_{t+1})]\\
\\
q_*(s,a) &= \mathbb{E}[r + \gamma \max_{a'} q_*(s', a')|s_t=s, a_t=a]\\
q_*(s_t,a_t) &= \mathbb{E}[r_{t+1} + \gamma \max_{a'} q_*(s_{t+1}, a')]\\
\end{aligned}
$$
- 벨만 기대 방정식과 같지만, $\pi$가 주어지는게 아니라 $\pi_*$ 를 사용하므로 $\mathbb{E}_\pi$ 대신 $\max_a \mathbb{E}$로 대체.

$$
\begin{aligned}
v_\pi (s) &= \sum_{a \in A} \pi(a|s) q_\pi(s,a)\\
v_*(s) &= \max_a q_*(s,a)\\
\end{aligned}
$$
- 상태 $s$의 최적 밸류는 $s$에서 선택 가능한 액션들 중 **밸류가 가장 높은 액션**의 밸류와 같다.
	- 이미 확정적으로 가장 가치있는 액션을 알고 있으므로 액션 확률 분포 $\pi(a|s)$를 따지는 것은 의미가 없음

$$
\begin{aligned}
q_\pi (s, a)&= r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_\pi(s')\\
q_* (s, a)&= r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_*(s')\\
\end{aligned}
$$
- 벨만 기대 방정식과 같다. 최적 밸류를 내는 정책을 쓰는 것만 다르다.

$$
\begin{aligned}
v_\pi (s) &= \sum_{a \in A} \pi(a|s) \left( r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_\pi(s') \right)\\
v_* (s) &= \max_a \left[ r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} v_*(s') \right]\\
\end{aligned}
$$
$$
\begin{aligned}
q_\pi (s, a)&= r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} \sum_{a' \in A} \pi(a'|s') q_\pi(s',a')\\
q_* (s, a)&= r^a_s + \gamma \sum_{s' \in S} P^a_{ss'} \max_{a'} q_*(s', a') \\
\end{aligned}
$$
