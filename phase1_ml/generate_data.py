"""
generate_data.py
----------------
Generates a synthetic dataset for mood prediction.

Features (STRICT – must not change later):
- sleep_hours
- screen_time
- physical_activity
- work_hours
- social_interaction
- caffeine_intake

Target:
- mood (0 = Low, 1 = Neutral, 2 = Good)
"""

import pandas as pd
import numpy as np

def generate_synthetic_data(
    samples: int = 1000,
    output_file: str = "mood_data.csv"
):
    try:
        np.random.seed(42)

        data = {
            "sleep_hours": np.random.uniform(4, 9, samples),
            "screen_time": np.random.uniform(2, 10, samples),
            "physical_activity": np.random.uniform(0, 3, samples),
            "work_hours": np.random.uniform(2, 12, samples),
            "social_interaction": np.random.uniform(0, 5, samples),
            "caffeine_intake": np.random.randint(0, 6, samples),
        }

        df = pd.DataFrame(data)

        # Simple rule-based mood generation (only for training signal)
        mood_score = (
            df["sleep_hours"] * 0.3
            - df["screen_time"] * 0.2
            + df["physical_activity"] * 0.4
            - df["work_hours"] * 0.1
            + df["social_interaction"] * 0.3
            - df["caffeine_intake"] * 0.1
        )

        df["mood"] = pd.cut(
            mood_score,
            bins=[-10, 1.5, 3.0, 10],
            labels=[0, 1, 2]
        ).astype(int)

        df.to_csv(output_file, index=False)
        print(f"[SUCCESS] Dataset generated: {output_file}")

    except Exception as e:
        print(f"[ERROR] Data generation failed: {e}")

if __name__ == "__main__":
    generate_synthetic_data()
