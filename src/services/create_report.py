import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import seaborn as sns
import pandas as pd



# Step 4: Generate a box plot for the 'Value' column
def plot_sentiment(df, col: str, title: str):
    df = pd.DataFrame(df)
    plt.figure(figsize=(8, 6))
    sns.countplot(x=df[col], stat='percent')
    plt.title(title)
    plt.ylabel("Percentage")
    plt.savefig(f"{title}_plot.png", dpi=300)
    plt.show()
    plt.close()



def create_pdf_report(response_dict: dict):
    response_dict = pd.DataFrame(response_dict)
    doc = SimpleDocTemplate("analysis_report.pdf")
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("Analysis of Customer satisfaction", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Add analysis results to the PDF
    elements.append(Paragraph("Analysis Results:", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Summary of positive reviews: {response_dict['positive_summary'].astype(str).tolist()}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Summary of negative reviews: {response_dict['negative_summary'].astype(str).tolist()}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Overall sentiment {response_dict['sentiment'].astype(str).tolist()}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f" {response_dict['service'].astype(str).tolist()}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Resize the image to fit within the PDF page
    max_width = 400  # Adjust as needed
    max_height = 300  # Adjust as needed
    elements.append(Image("./Sentiment_Analysis_plot.png", width=max_width, height=max_height))

    doc.build(elements)

