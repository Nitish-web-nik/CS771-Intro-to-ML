import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.linalg import khatri_rao

class LinearCARPUF:
    def __init__(self, threshold):
        self.threshold = threshold
        self.model = LogisticRegression()
        self.poly = PolynomialFeatures(degree=2)

    def my_map(self, challenges):
        num_samples = challenges.shape[0]
        num_bits = challenges.shape[1]
        
        # Initialize empty array to store mapped features
        mapped_features = np.zeros((num_samples, num_bits * num_bits))
        
        # Compute Khatri-Rao product for each sample
        for i in range(num_samples):
            upper_signal = challenges[i]
            lower_signal = 1 - challenges[i]
            
            # Compute Khatri-Rao product of upper and lower signals
            mapped_feature = np.kron(upper_signal, lower_signal)
            
            # Store mapped feature
            mapped_features[i] = mapped_feature

        return mapped_features



    def my_fit(self, challenges, responses):
        """
        Trains the linear model using the mapped challenges and responses.
        """

        mapped_challenges = self.my_map(challenges)
        self.model.fit(mapped_challenges, responses)
        # Compute training accuracy
        # predictions_train = carpuf.predict(challenges, responses)
        # train_accuracy = np.mean(predictions_train == responses) * 100
        # print("Training Accuracy:", train_accuracy, "%")


    def predict(self, challenges, responses):
        """
        Predicts the responses for the given challenges.
        """
        mapped_challenges = self.my_map(challenges)
        predictions = self.model.predict(mapped_challenges)
        test_accuracy = np.mean(predictions == responses) * 100
        print("Predictions on test dataset:", test_accuracy)

    

carpuf = LinearCARPUF(threshold=0.5)

challenges = []
responses = []

filename = 'train.dat'

test_dat_file = 'test.dat'

# print("Test Challenge Vectors:")
# print(test_challenges[:5])
# print("Test Responses:")
# print(test_responses[:5])

carpuf = LinearCARPUF(threshold=0.5)

# Read challenge vectors and responses from train dataset file
train_challenges = np.loadtxt(filename, usecols=range(32), dtype=int)
train_responses = np.loadtxt(filename, usecols=32, dtype=int)

# Train the model using the training challenge-response pairs
carpuf.my_fit(train_challenges, train_responses)

test_challenges = np.loadtxt(test_dat_file, usecols=range(32), dtype=int)
test_responses = np.loadtxt(test_dat_file, usecols=32, dtype=int)

carpuf.predict(test_challenges, test_responses)
