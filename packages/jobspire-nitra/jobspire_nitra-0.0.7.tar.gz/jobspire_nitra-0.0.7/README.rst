==============================================
JobSpire truth table remote control python lib
==============================================

----------------
How to implement
----------------

.. code-block:: python

  # establish connection with jobspire
  nitra = Nitra(
    username='username',
    secret='secret password',
    base_url='http://full_jobspire_url.dk/nitra',
    ensure_connected=True
  )

  # usage:
  nitra.get_skills()
  nitra.get_job_areas()
  nitra.insert_job_postings(List[dict])
  nitra.insert_job_posting_skills(List[dict])
  nitra.delete_job_postings_by_source_id(source_ids: List[str])
  nitra.ping()

-----------
Development
-----------

To build:
``python3 -m build``

To release:
``./release.sh``
