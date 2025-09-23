import matplotlib.pyplot as plt
import numpy as np

# Sample data (synthetic, replace with real values if available)
np.random.seed(42)
distance = np.linspace(0, 2, 40)   # From 0 to 2 km
eqs_scores = np.random.randint(-15, 15, size=40)  # EQS scores

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bar chart (similar to original)
bars = ax.bar(distance, eqs_scores, width=0.02, color="royalblue", linewidth=0.5)

# Regression line (example: y = -0.005x - 3)
x_line = np.linspace(0, 2, 100)
y_line = -0.005 * x_line - 3
ax.plot(x_line, y_line, color="blue", linestyle="--")

# Axis labels and title
ax.set_title("EQS Score  ", fontsize=14, fontweight="bold", loc="left")
ax.text(0.6, 19, "With The Distance", fontsize=12, color="purple", style="italic")

ax.set_xlabel("Distance from Victoria Harbour (km)", fontsize=12)
ax.set_ylabel("Environmental Quality Survey (EQS) Score", fontsize=12)

# Grid & limits
ax.axhline(0, color="black", linewidth=1)
ax.set_xlim(0, 2)
ax.set_ylim(-20, 20)
ax.grid(alpha=0.4)

# Custom legend
ax.legend(["EQS score"], loc="upper right")

# Annotation for equation
ax.text(1.1, -12, r"$Y = -0.005x - 3$", fontsize=12, color="blue", rotation=0)

# Caption below plot
plt.figtext(0.5, -0.05, 
            "Graph showing the change of environments quality survey (EQS)  while the distance\n"
            "from Victoria Harbour increases", 
            wrap=True, horizontalalignment="center", fontsize=11, style="italic")

plt.tight_layout()
plt.show()