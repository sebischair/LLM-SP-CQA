def clean_prediction(prediction: str) -> str:
    prediction = f"{prediction}"
    prediction = prediction.replace("\n", " ")

    # remove "SPARQL query:" that is added due to few-shot examples
    prediction = prediction.replace("SPARQL query:", " ")

    # remove everything after separator "<\s>" (LLaMA few-shot)
    prediction = prediction.split("</s>")[0]

    # add spaces arount "."
    prediction = prediction.replace(".", " . ")

    # add a space before ?
    prediction = prediction.replace("?", " ?")

    # remove duplicate spaces
    prediction = " ".join(prediction.split())

    # remove leading and trailing spaces
    prediction = prediction.strip()

    return prediction