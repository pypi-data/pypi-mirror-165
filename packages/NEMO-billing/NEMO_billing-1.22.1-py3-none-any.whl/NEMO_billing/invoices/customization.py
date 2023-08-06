from typing import Dict

from NEMO.decorators import customization
from NEMO.views.customization import CustomizationBase
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


@customization(key="invoices", title="Invoices")
class InvoiceCustomization(CustomizationBase):
    variables = {"invoice_number_format": "{:04d}", "invoice_number_current": "0"}
    files = [
        ("email_send_invoice_subject", ".txt"),
        ("email_send_invoice_message", ".html"),
        ("email_send_invoice_reminder_subject", ".txt"),
        ("email_send_invoice_reminder_message", ".html"),
    ]

    def context(self) -> Dict:
        # Adding invoice number formatted to the template
        customization_context = super().context()
        try:
            customization_context["invoice_number_formatted"] = self.get("invoice_number_format").format(
                int(self.get("invoice_number_current"))
            )
        except:
            pass
        return customization_context

    def validate(self, name, value):
        if name == "invoice_number_format":
            try:
                value.format(123)
            except Exception as e:
                raise ValidationError(str(e))


@customization(key="billing", title="Billing")
class BillingCustomization(CustomizationBase):
    variables = {
        "billing_accounting_email_address": "",
        "billing_project_expiration_reminder_days": "",
        "billing_project_expiration_reminder_cc": "",
    }
    files = [
        ("billing_project_expiration_reminder_email_subject", ".txt"),
        ("billing_project_expiration_reminder_email_message", ".html"),
    ]

    def validate(self, name, value):
        if name == "billing_project_expiration_reminder_days" and value:
            # Check that we have an integer or a list of integers
            try:
                for reminder_days in value.split(","):
                    try:
                        int(reminder_days)
                    except ValueError:
                        raise ValidationError(f"{reminder_days} is not a valid integer")
            except ValidationError:
                raise
            except Exception as e:
                raise ValidationError(str(e))
        elif name == "billing_accounting_email_address" and value:
            validate_email(value)
        elif name == "billing_project_expiration_reminder_cc":
            recipients = tuple([e for e in value.split(",") if e])
            for email in recipients:
                validate_email(email)
