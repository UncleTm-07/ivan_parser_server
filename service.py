import sys, requests, json, time, re
import traceback
from urllib.parse import urlparse

from schemas import NewWorker, Worker


async def get_orcid_id_by_name(worker_data: NewWorker):
    try:
        if worker_data:
            lastname = worker_data.lastName.lower()
            name = worker_data.name.lower()
            r = requests.get(
                f"https://pub.orcid.org/v3.0/expanded-search/?q=(given-names:{name}) AND (family-name:{lastname})&start=0&rows=50",
                headers={"Accept": "application/vnd.orcid+json"})
            result = json.loads(r.text)
            expanded_result = result["expanded-result"][0] if result["expanded-result"] else ""
            orcid_id = expanded_result["orcid-id"] if expanded_result != "" else "Orcid ID not found"
            return orcid_id
    except Exception as e:
        print("Під-час пошуку Orcid ID виникла помилка!!")
        print(e)
        return "Orcid ID not found"


async def get_works_of_worker(worker: Worker):
    works = []
    if worker.orcid_id != "Orcid ID not found":
        orcid_data = {
            "website_name": "Orcid",
            "data": []
        }
        res = await get_orcid_work(worker.orcid_id)
        if res and len(res) > 0:
            orcid_data["data"] = res
            works.append(orcid_data)

    return works


async def get_orcid_work(orcid_id):
    print(orcid_id)
    response = []
    try:
        r = requests.get(f"https://pub.orcid.org/v3.0/{orcid_id}/works",
                         headers={"Accept": "application/vnd.orcid+json"})
        result = json.loads(r.text)
        groups = result["group"] if result is not None and result["group"] is not None else None

        if groups is None:
            return None

        for group in groups:
            work = group["work-summary"][0] if group["work-summary"] else None

            if work is not None:
                title = get_title(work["title"]) if work["title"] else ""
                journal_title = get_journal_title(work["journal-title"]) if work["journal-title"] else ""
                publication_date = get_publication_date(work["publication-date"]) if work["publication-date"] else ""
                source = get_source(work["url"]) if work["url"] else ""

                data = {
                    "title": title,
                    "journal_title": journal_title,
                    "publication_date": publication_date,
                    "source": source,
                }
                response.append(data)
        return response
    except Exception as e:
        print("Під-час парсингу виникла помилка!!")
        print(e)
        return []


def get_title(work_title):
    title = work_title["title"] if work_title["title"] else ""
    value = title["value"] if title["value"] else ""
    return value


def get_journal_title(journal_title):
    value = journal_title["value"] if journal_title["value"] else ""
    return value


def get_publication_date(publication_date):
    publication_date_year = publication_date["year"] if publication_date["year"] else ""
    publication_date_year_value = publication_date_year["value"] if publication_date_year else None
    return publication_date_year_value


def get_source(url):
    value = url["value"] if url["value"] else ""
    return value
