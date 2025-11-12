import random
from dataclasses import dataclass

@dataclass
class Tsetlin:
    n: int = 4             # states per action
    action1: str = "No"     # states 1..n
    action2: str = "Yes"    # states n+1..2n

    def __post_init__(self):
        # start at the boundary between the two actions
        self.state = random.choice([self.n, self.n + 1])

    # Reward rule
    def reward(self):
        if self.state <= self.n and self.state > 1:
            self.state -= 1
        elif self.state > self.n and self.state < 2 * self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        else:
            self.state -= 1

    # Decision rule
    def decide(self) -> str:
        return self.action1 if self.state <= self.n else self.action2


def reward_prob_from_M(M: int) -> float:
    # Assignment rule
    if 0 <= M <= 3:
        return M * 0.2
    elif M in (4, 5):
        return 0.6 - (M - 3) * 0.2


def run_experiment(num_steps: int = 10_000, n_states_per_action: int = 4):
    

    # 1) Create 5 Tsetlin Automata with actions "No" and "Yes"
    automata = [Tsetlin(n=n_states_per_action, action1="No", action2="Yes") for _ in range(5)]

    history_M = []    # how many "Yes" at each step
    action_counts = [0] * len(automata)

    for t in range(num_steps):
        # 2) Count how many say "Yes"
        decisions = [a.decide() for a in automata]
        M = sum(1 for d in decisions if d == "Yes")
        history_M.append(M)
        for i, d in enumerate(decisions):
            if d == "Yes":
                action_counts[i] += 1

        # 3) Compute reward probability p from M
        p = reward_prob_from_M(M)

        # 3) Give each automaton an independent reward with prob p, else a penalty
        for a in automata:
            if random.random() < p:
                a.reward()
            else:
                a.penalize()
        # 4) goto 2 (loop continues)
    
    

    # Results
    avg_M = sum(history_M) / len(history_M)
    final_decisions = [a.decide() for a in automata]

    print(f"Steps: {num_steps}")
    print(f"Distribution of M over last 100 steps: {history_M[-100:]}")
    print(f"Final decisions of the 5 automata: {final_decisions}")
    print(f"Average Yes: {avg_M:.2f}")
    print("Per-automaton fraction of 'Yes' during run:",
          [round(c / num_steps, 3) for c in action_counts])



if __name__ == "__main__":
    run_experiment(num_steps=10000, n_states_per_action=4)
