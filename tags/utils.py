import pywikibot


def get_wikidata_info(qid):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    item = pywikibot.ItemPage(repo, qid)
    item.get()

    label = item.labels["en"]
    description = item.descriptions.get("en", "")

    return {"label": label, "description": description}
