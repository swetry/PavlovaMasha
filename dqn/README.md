# Отчет по заданию 18: Reinforcement Learning DQN для игры
## 1. Полное задание из методички:
Вариант 18: Reinforcement Learning DQN для игры

Задача: Реализовать Deep Q-Network (DQN) для обучения агента играть в игру.

Требования:

DQN архитектура с target network

Experience replay buffer

Epsilon-greedy exploration

Визуализация обучения

Что нужно дополнить в коде-заготовке:

Q-network архитектуру

Replay buffer

Epsilon-greedy стратегию

Replay function для обучения на batch

Target network обновление

Основной цикл обучения

Визуализацию learning curves

## 2. Алгоритм работы по блокам:


1) Блок импорта библиотек

        python
        import numpy as np
        import random
        import collections
        import matplotlib.pyplot as plt
        import gym
        from typing import List, Tuple, Deque
        import pickle


2) Блок определения класса NeuralNetwork


        class NeuralNetwork:
            def __init__(self, input_size, hidden_sizes, output_size):
                # Инициализация весов
                self.weights = []
                self.biases = []
                
                # Создание слоев
                prev_size = input_size
                for hidden_size in hidden_sizes:
                    self.weights.append(np.random.randn(prev_size, hidden_size) * 0.1)
                    self.biases.append(np.zeros(hidden_size))
                    prev_size = hidden_size
                
                # Выходной слой
                self.weights.append(np.random.randn(prev_size, output_size) * 0.1)
                self.biases.append(np.zeros(output_size))
            
            def relu(self, x):
                return np.maximum(0, x)
            
            def relu_derivative(self, x):
                return (x > 0).astype(float)
            
            def forward(self, x, training=False):
                # Прямой проход через слои
                self.activations = [x]
                self.z_values = []
                current = x
                
                # Скрытые слои с ReLU
                for i in range(len(self.hidden_sizes)):
                    z = np.dot(current, self.weights[i]) + self.biases[i]
                    self.z_values.append(z)
                    current = self.relu(z)
                    self.activations.append(current)
                
                # Выходной слой (линейный)
                z = np.dot(current, self.weights[-1]) + self.biases[-1]
                self.z_values.append(z)
                self.activations.append(z)
                
                return self.activations[-1]
            
            def backward(self, x, y, learning_rate=0.001):
                # Вычисление градиентов и обновление весов
                m = x.shape[0]
                error = self.activations[-1] - y
                dZ = error / m
                
                # Обратное распространение
                gradients = []
                for i in reversed(range(len(self.weights))):
                    if i == len(self.weights) - 1:
                        dW = np.dot(self.activations[-2].T, dZ)
                        db = np.sum(dZ, axis=0)
                        dA_prev = np.dot(dZ, self.weights[i].T)
                    else:
                        dZ = dA_prev * self.relu_derivative(self.z_values[i])
                        dW = np.dot(self.activations[i].T, dZ)
                        db = np.sum(dZ, axis=0)
                        dA_prev = np.dot(dZ, self.weights[i].T)
                    
                    gradients.insert(0, (dW, db))
                
                # Обновление весов
                for i in range(len(self.weights)):
                    self.weights[i] -= learning_rate * gradients[i][0]
                    self.biases[i] -= learning_rate * gradients[i][1]
                
                return np.mean(error ** 2)

   
3) Блок определения класса DQNAgent

        class DQNAgent:
            def __init__(self, state_size, action_size, learning_rate=0.001):
                self.state_size = state_size
                self.action_size = action_size
                
                # Создание Q-network и target network
                self.q_network = NeuralNetwork(state_size, [64, 64], action_size)
                self.target_network = NeuralNetwork(state_size, [64, 64], action_size)
                
                # Инициализация replay buffer
                self.replay_buffer = collections.deque(maxlen=2000)
                
                # Гиперпараметры
                self.gamma = 0.99
                self.epsilon = 1.0
                self.epsilon_decay = 0.995
                self.epsilon_min = 0.01
                self.batch_size = 32
            
            def remember(self, state, action, reward, next_state, done):
                # Сохранение опыта в буфер
                self.replay_buffer.append((state, action, reward, next_state, done))
            
            def act(self, state, training=True):
                # Epsilon-greedy стратегия
                if training and np.random.rand() <= self.epsilon:
                    return np.random.randint(self.action_size)
                
                q_values = self.q_network.forward(state[np.newaxis])
                return np.argmax(q_values[0])
            
            def replay(self, batch_size):
                # Обучение на batch из replay buffer
                if len(self.replay_buffer) < batch_size:
                    return 0.0
                
                # Выбор случайного батча
                batch = random.sample(self.replay_buffer, batch_size)
                states, actions, rewards, next_states, dones = zip(*batch)
                
                states = np.array(states)
                actions = np.array(actions)
                rewards = np.array(rewards)
                next_states = np.array(next_states)
                dones = np.array(dones)
                
                # Вычисление target Q-values
                next_q_values = self.target_network.forward(next_states)
                max_next_q = np.max(next_q_values, axis=1)
                target_q = rewards + self.gamma * max_next_q * (1 - dones)
                
                # Обучение сети
                current_q = self.q_network.forward(states)
                current_q[np.arange(batch_size), actions] = target_q
                loss = self.q_network.backward(states, current_q, 0.001)
                
                return loss
            
            def update_target_network(self):
                # Обновление target network
                weights, biases = self.q_network.get_weights()
                self.target_network.set_weights(weights, biases)

   
4) Блок основной функции Main()
        
        def main():
            #Загрузка и подготовка среды
            env = gym.make('CartPole-v1')
            state_size = env.observation_space.shape[0]
            action_size = env.action_space.n
            
            #Инициализация модели
            agent = DQNAgent(state_size, action_size)
            
            #Цикл обучения
            episode_rewards = []
            for episode in range(100):
                state, _ = env.reset()
                total_reward = 0
                done = False
                
                while not done:
                    # Выбор действия
                    action = agent.act(state)
                    next_state, reward, done, truncated, _ = env.step(action)
                    done = done or truncated
                    
                    # Сохранение опыта
                    agent.remember(state, action, reward, next_state, done)
                    
                    # Обучение
                    agent.replay(agent.batch_size)
                    
                    # Обновление состояния
                    state = next_state
                    total_reward += reward
                
                # Уменьшение epsilon
                if agent.epsilon > agent.epsilon_min:
                    agent.epsilon *= agent.epsilon_decay
                
                episode_rewards.append(total_reward)
                
                # Периодическое обновление target network
                if episode % 10 == 0:
                    agent.update_target_network()
                
                if (episode + 1) % 10 == 0:
                    print(f"Эпизод {episode+1}, Награда: {total_reward}, Epsilon: {agent.epsilon:.3f}")
            
            env.close()
            
            #Визуализация результатов
            plt.figure(figsize=(12, 5))
            plt.subplot(1, 2, 1)
            plt.plot(episode_rewards)
            plt.title('Награды за эпизоды')
            plt.xlabel('Эпизод')
            plt.ylabel('Награда')
            
            plt.subplot(1, 2, 2)
            window = 10
            moving_avg = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
            plt.plot(moving_avg)
            plt.title(f'Скользящее среднее (окно={window})')
            plt.xlabel('Эпизод')
            plt.ylabel('Награда')
            
            plt.tight_layout()
            plt.savefig('dqn_results.png', dpi=300)
            plt.show()

   
5) Блок выполнения программы

        if __name__ == "__main__":
            main()

   
## 3. Ответ на контрольный вопрос:
Вопрос 18: Как Affinity Propagation автоматически определяет количество кластеров?


Affinity Propagation автоматически определяет количество кластеров через итеративную конкуренцию точек данных за роль центров (exemplars). Алгоритм использует обмен сообщениями (responsibility и availability), в ходе которого exemplars выявляются на основе взаимного сходства точек. Ключевой параметр preference регулирует число кластеров: высокое значение ведет к увеличению центров, низкое — к их уменьшению.
Сходимость: Процесс продолжается до стабилизации набора exemplars — они и становятся центрами кластеров.
Преимущество: Алгоритм самостоятельно выявляет естественное число кластеров, исходя из структуры данных, без предварительных предположений или эвристик.

Итог: Число кластеров не задается заранее, а возникает естественным образом в процессе работы алгоритма.
