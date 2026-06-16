import pandas as pd
import chromadb
import uuid


class Portfolio:

    def __init__(self, file_path="app/resources/my_portfolio.csv"):

        self.file_path = file_path

        self.data = pd.read_csv(file_path)

        self.chroma_client = chromadb.PersistentClient(
            path="vectorstore"
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="portfolio"
        )

    def load_portfolio(self): 

        if self.collection.count() == 0:

            for _, row in self.data.iterrows():

                self.collection.add(
                    documents=[str(row["Techstack"])],
                    metadatas=[
                        {
                            "links": str(row["Links"])
                        }
                    ],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):

        if not skills:
            return []

        query = " ".join(skills)

        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )

        metadata = results.get("metadatas", [])

        links = []

        if metadata:

            for item in metadata[0]:

                link = item.get("links")

                if link and link not in links:
                    links.append(link)

        return links 