test: unit acceptance

acceptance:
	@echo ==============================================
	@echo ========= Running acceptance specs ===========
	@python manage.py harvest
	@echo

unit:
	@echo =======================================
	@echo ========= Running unit specs ==========
	@python manage.py test bank_system
	@echo

