PYTHON ?= .venv/bin/python
PYTHONPATH_VALUE := src

.PHONY: test evidence benchmark readiness dry-run provider provider-once croo-activity

test:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m unittest discover -s tests

evidence:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/run_all_evidence.py

benchmark:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/run_benchmark.py

readiness:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/check_live_readiness.py

dry-run:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/run_live_dry_run.py

provider:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/run_croo_provider.py

provider-once:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/run_croo_provider.py --once

croo-activity:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) examples/check_croo_activity.py --include-all-services
