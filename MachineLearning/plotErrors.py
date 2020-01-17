import matplotlib.pyplot as plt

# Create variables that correspond to model errors and sampling frequency
freq = [55, 60, 75, 100, 200, 300, 400]
errors = [169, 112, 103, 94, 41, 35, 68]

# Plot graph
plt.plot(freq, errors)
plt.xlabel('Frequency')
plt.ylabel('Errors')
plt.title('Model Accuracy for Different Sampling Frequencies')
plt.show()