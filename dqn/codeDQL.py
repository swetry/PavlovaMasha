!pip install "gymnasium[classic-control]" --quiet

import gymnasium as gym
import numpy as np
import random
import collections
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, optimizers, losses, Model

class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        learning_rate=0.0005,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        buffer_size=20000,
        tau=1.0
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate

        self.q_network = self._build_q_network()
        self.target_network = self._build_q_network()
        self.target_network.set_weights(self.q_network.get_weights())

        self.optimizer = optimizers.Adam(learning_rate=self.learning_rate)
        self.loss_fn = losses.MeanSquaredError()

        self.replay_buffer = collections.deque(maxlen=buffer_size)

        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.tau = tau

    def _build_q_network(self):
        inputs = layers.Input(shape=(self.state_size,))
        x = layers.Dense(64, activation='relu')(inputs)
        x = layers.Dense(64, activation='relu')(x)
        outputs = layers.Dense(self.action_size)(x)
        model = Model(inputs=inputs, outputs=outputs)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def act(self, state, training=True):
        if training and np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        state = np.array(state, dtype=np.float32)[np.newaxis, ...]
        q_values = self.q_network(state).numpy()[0]
        return np.argmax(q_values)

    def replay(self, batch_size=64):
        if len(self.replay_buffer) < batch_size:
            return None

        batch = random.sample(self.replay_buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = tf.convert_to_tensor(np.array(states, dtype=np.float32))
        next_states = tf.convert_to_tensor(np.array(next_states, dtype=np.float32))
        actions = tf.convert_to_tensor(actions, dtype=tf.int32)
        rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)
        dones = tf.convert_to_tensor(dones, dtype=tf.float32)

        next_q = self.target_network(next_states)
        max_next_q = tf.reduce_max(next_q, axis=1)
        target_q = rewards + self.gamma * max_next_q * (1.0 - dones)

        with tf.GradientTape() as tape:
            q_values_all = self.q_network(states)
            indices = tf.stack([tf.range(batch_size), actions], axis=1)
            q_values = tf.gather_nd(q_values_all, indices)
            loss = self.loss_fn(target_q, q_values)

        grads = tape.gradient(loss, self.q_network.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.q_network.trainable_variables))

        return float(loss.numpy())

    def update_target_network(self):
        if self.tau >= 1.0:
            self.target_network.set_weights(self.q_network.get_weights())
        else:
            q_weights = self.q_network.get_weights()
            tgt_weights = self.target_network.get_weights()
            new_weights = []
            for qw, tw in zip(q_weights, tgt_weights):
                new_weights.append(self.tau * qw + (1.0 - self.tau) * tw)
            self.target_network.set_weights(new_weights)

def train_dqn(
    env_name="CartPole-v1",
    episodes=300,
    batch_size=64,
    update_frequency=5,
    render=False
):
    env = gym.make(env_name)
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = DQNAgent(
        state_size=state_size,
        action_size=action_size,
        learning_rate=0.0005,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        buffer_size=20000,
        tau=1.0
    )

    episode_rewards = []
    episode_losses = []

    for episode in range(episodes):
        state, info = env.reset()
        done = False
        total_reward = 0.0
        losses = []

        while not done:
            if render:
                env.render()

            action = agent.act(state, training=True)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            if done and total_reward < 500:
                reward = reward - 1.0

            agent.remember(state, action, reward, next_state, float(done))
            state = next_state
            total_reward += reward

            loss = agent.replay(batch_size)
            if loss is not None:
                losses.append(loss)

        if episode % update_frequency == 0:
            agent.update_target_network()

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay
            agent.epsilon = max(agent.epsilon_min, agent.epsilon)

        episode_rewards.append(total_reward)
        episode_losses.append(np.mean(losses) if len(losses) > 0 else np.nan)

        print(
            f"Episode {episode+1}/{episodes} | "
            f"Reward: {total_reward:.1f} | "
            f"Epsilon: {agent.epsilon:.3f} | "
            f"Loss: {episode_losses[-1]:.4f}"
        )

    env.close()
    return agent, episode_rewards, episode_losses

agent, rewards, losses = train_dqn(
    episodes=300,
    batch_size=64,
    update_frequency=5,
    render=False
)

def moving_average(x, window=10):
    if len(x) < window:
        return x
    return np.convolve(x, np.ones(window)/window, mode='valid')

plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.plot(rewards, alpha=0.4, label="Reward per episode")
plt.plot(range(len(moving_average(rewards, 10))), moving_average(rewards, 10),
         label="Moving avg (10)", color="red")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("DQN: Reward")
plt.legend()

plt.subplot(1,2,2)
plt.plot(losses, alpha=0.4, label="Loss per episode")
clean_losses = [l for l in losses if not np.isnan(l)]
if len(clean_losses) >= 10:
    ma_loss = moving_average(clean_losses, 10)
    plt.plot(range(len(ma_loss)), ma_loss,
             label="Moving avg (10)", color="red")
plt.xlabel("Episode")
plt.ylabel("Loss")
plt.title("DQN: Training loss")
plt.legend()

plt.tight_layout()
plt.show()

def run_trained_agent(env_name, agent, episodes=5):
    env = gym.make(env_name, render_mode="human")
    for ep in range(episodes):
        state, info = env.reset()
        done = False
        total_reward = 0
        while not done:
            env.render()
            action = agent.act(state, training=False)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            state = next_state
            total_reward += reward
        print(f"Test episode {ep+1}: reward = {total_reward}")
    env.close()

# Пример запуска после обучения:
# run_trained_agent("CartPole-v1", agent, episodes=3)

#ВИЗУАЛИЗАЦИЯ
import matplotlib.pyplot as plt
import numpy as np

def moving_average(x, window=10):
    if len(x) < window:
        return x
    return np.convolve(x, np.ones(window) / window, mode="valid")

# Если нет отдельной валидации – используем обучающие награды как вал.
rewards_train = rewards
rewards_val = rewards  # или список из отдельного тестового прогона

# ---------------- 1) Training Loss Progression ----------------
plt.figure(figsize=(10, 4))
plt.plot(losses, color="#d62728", linewidth=2.5, label="Training Loss")

clean_losses = [l for l in losses if not np.isnan(l)]
if len(clean_losses) > 0:
    final_loss = clean_losses[-1]
    plt.annotate(
        f"Final Loss: {final_loss:.4f}",
        xy=(len(losses) - 1, final_loss),
        xytext=(10, max(clean_losses)),
        bbox=dict(boxstyle="round", fc="white", ec="gray"),
        arrowprops=dict(arrowstyle="->", color="gray")
    )

plt.title("Training Loss Progression")
plt.xlabel("Episode")
plt.ylabel("Loss")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ------------- 2) Model Reward Progression (аналог accuracy) -------------
plt.figure(figsize=(12, 4))

ma_train = moving_average(rewards_train, window=10)
ma_val = moving_average(rewards_val, window=10)

plt.plot(ma_train, label="Training Reward", color="#1f77b4", linewidth=2.5)
plt.plot(ma_val, label="Validation Reward", color="#ff7f0e", linewidth=2.5)

target_reward = 195
plt.axhline(target_reward, color="red", linestyle="--", linewidth=1.5,
            label=f"Target ({target_reward})")

plt.title("Model Reward Progression")
plt.xlabel("Episode")
plt.ylabel("Reward (moving avg)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ------- 3) «Precision and Recall Metrics»‑стиль для наград -------
plt.figure(figsize=(12, 4))

episodes_axis = np.arange(len(ma_train))

plt.plot(episodes_axis, ma_train, label="Training Reward", color="#2ca02c", linewidth=2.5)
plt.plot(episodes_axis[:len(ma_val)], ma_val, label="Validation Reward",
         color="#9467bd", linewidth=2.5)

plt.axhline(target_reward, color="red", linestyle="--", linewidth=1.5,
            label="Target")

plt.fill_between(
    episodes_axis[:len(ma_val)],
    ma_train[:len(ma_val)],
    ma_val,
    color="#c5b0d5",
    alpha=0.3
)

plt.title("Reward Metrics (Train vs Validation)")
plt.xlabel("Episode")
plt.ylabel("Reward (moving avg)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# --------------- 4) Final Model Performance Metrics (bar) ---------------
final_train = ma_train[-1]
final_val = ma_val[-1]
max_train = float(np.max(rewards_train))
max_val = float(np.max(rewards_val))

metrics = [final_train, final_val, max_train, max_val]
labels = ["Train\nReward", "Val\nReward", "Max\nTrain", "Max\nVal"]

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, metrics,
               color=["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"])

for bar, val in zip(bars, metrics):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 1,
             f"{val:.1f}", ha="center", va="bottom", fontsize=11)

plt.axhline(target_reward, color="red", linestyle="--", linewidth=1.5,
            label=f"Target ({target_reward})")

plt.title("Final Model Performance Metrics")
plt.ylabel("Reward")
plt.ylim(0, max(max(metrics) + 10, target_reward + 10))
plt.grid(axis="y", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
