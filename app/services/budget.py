import pandas as pd
import matplotlib.pyplot as plt

class Budget:
    def __init__(self, budget_dict):
        self.budget = budget_dict
        self.budget_df = pd.DataFrame(list(budget_dict.items()), columns=['category', 'budgeted_amount'])

    def calculate_spending(self, transactions_df):
        # Group transactions by budget category and sum the amounts
        spending_df = transactions_df.groupby('budget_category')['amount'].sum().reset_index()
        spending_df.columns = ['category', 'spent_amount']

        # Merge with budget
        self.budget_summary_df = pd.merge(self.budget_df, spending_df, on='category', how='left')
        self.budget_summary_df['spent_amount'] = self.budget_summary_df['spent_amount'].fillna(0)

        # Exclude "Income" from spending and remaining budget calculations
        self.budget_summary_df = self.budget_summary_df[self.budget_summary_df['category'] != 'Income']

        # Calculate remaining budget
        self.budget_summary_df['remaining_budget'] = self.budget_summary_df['budgeted_amount'] - self.budget_summary_df['spent_amount']

    def display_budget_summary(self):
        print("\nBudget Summary:")
        print(self.budget_summary_df)

    # Visualization method for a single category (Progress bar with rounded edges using plt.barh)
    def plot_category_progress_bar(self, category):
        # Filter the budget summary for the specific category
        row = self.budget_summary_df[self.budget_summary_df['category'] == category].iloc[0]

        spent_amount = abs(row['spent_amount'])
        budgeted_amount = row['budgeted_amount']
        remaining_amount = budgeted_amount - spent_amount

        # Set the colors based on the spending status
        if remaining_amount >= 0:
            bar_color = 'green' if remaining_amount > 0.2 * budgeted_amount else 'yellow'  # Green if more than 20% remains
        else:
            bar_color = 'red'  # Red for overspending

        # Create the figure and axis for the plot
        fig, ax = plt.subplots(figsize=(8, 1))  # Skinnier bar with a smaller height

        # Plot the spent amount bar with rounded edges
        ax.barh(0, spent_amount, color=bar_color, height=0.4, edgecolor='none')

        # Plot the remaining amount bar (in light gray) if under budget
        if remaining_amount > 0:
            ax.barh(0, remaining_amount, color='lightgray', left=spent_amount, height=0.4, edgecolor='none')

        # Format the text labels for spent and total budget
        # Escape the dollar signs in case there's any special interpretation issue
        spent_label = f"\${spent_amount:.0f} of \${budgeted_amount:.0f}"
        remaining_label = f"\${remaining_amount:.0f} Left" if remaining_amount >= 0 else f"\${abs(remaining_amount):.0f} Over"

        # Choose contrasting text color for better visibility
        text_color = 'white' if bar_color != 'lightgray' else 'black'

        # Add text on the bar (ensure spent_amount is large enough for text to fit)
        if spent_amount > 0:
            ax.text(spent_amount / 2, 0, spent_label, va='center', ha='center', color=text_color, fontsize=10,
                    fontweight='bold')
        else:
            ax.text(5, 0, spent_label, va='center', ha='center', color=text_color, fontsize=10, fontweight='bold')

        # Add the remaining/over text on the right side of the bar
        ax.text(budgeted_amount + 10, 0, remaining_label, va='center', ha='left', fontsize=12, fontweight='bold',
                color='black' if remaining_amount >= 0 else 'red')

        # Remove axes for a cleaner look
        ax.set_xlim(0, budgeted_amount * 1.1)  # Limit the x-axis to 110% of the budget for padding
        ax.set_yticks([])  # Remove y-ticks
        ax.set_xticks([])  # Remove x-ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Set title as the category name
        ax.set_title(category, loc='left', fontsize=12, fontweight='bold', pad=10)

        plt.box(False)  # Remove the box around the chart for a cleaner look
        plt.tight_layout()
        plt.show()

    # Visualization method for Donut Chart (with side legend and total spending in center)
    def plot_donut_chart_with_legend(self):
        # Convert spent amounts to absolute values for correct representation
        spent_amounts = self.budget_summary_df['spent_amount'].abs()
        categories = self.budget_summary_df['category']

        # Create a color palette (you can customize this with your preferred colors)
        colors = plt.get_cmap('tab20c').colors  # Using a nice built-in colormap

        # Calculate the total spent amount
        total_spent = spent_amounts.sum()

        # Create the pie chart and make it a donut
        plt.figure(figsize=(8, 6))
        wedges, texts = plt.pie(
            spent_amounts,
            startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='w'),  # Width makes it a donut chart, edgecolor for clean separation
            colors=colors[:len(categories)],  # Use as many colors as there are categories
            counterclock=False
        )

        # Add a label in the center of the donut chart (showing total spending)
        plt.text(0, 0, f'Total spending\n${total_spent:.2f}', ha='center', va='center', fontsize=14, fontweight='bold')

        # Add a title with improved styling
        plt.title('Spending Distribution by Category', fontsize=16, fontweight='bold', pad=20)

        # Add a legend on the side with category names and corresponding colors
        plt.legend(
            wedges, categories,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),  # Position the legend outside to the right of the chart
            fontsize=12
        )

        # Remove any extra space
        plt.tight_layout()

        # Show the chart
        plt.show()