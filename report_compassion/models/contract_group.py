##############################################################################
#
#    Copyright (C) 2015 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __manifest__.py
#
##############################################################################
import logging
import math
from datetime import datetime

from babel.dates import format_date

from odoo import api, models, fields, _
from odoo.exceptions import Warning as odooWarning
from odoo.tools import mod10r

logger = logging.getLogger(__name__)

COMPASSION_BVR = "01-44443-7"


class ContractGroup(models.Model):
    _inherit = "recurring.contract.group"

    scan_line = fields.Char(compute="_compute_scan_line")
    format_ref = fields.Char(compute="_compute_format_ref")

    @api.multi
    def _compute_scan_line(self):
        """ Generate a scan line for contract group. """
        acc_number = self.get_company_bvr_account()
        for group in self.filtered("bvr_reference"):
            group.scan_line = self.get_scan_line(acc_number, group.bvr_reference)

    @api.multi
    def compute_scan_line(self, start, stop, sponsorships):
        """ Generate a scan line for contract group. """
        self.ensure_one()
        acc_number = self.get_company_bvr_account()
        amount = self._get_amount(start, stop, sponsorships)
        return self.get_scan_line(acc_number, self.bvr_reference, amount)

    @api.multi
    def _compute_format_ref(self):
        slip_obj = self.env["l10n_ch.payment_slip"]
        for group in self:
            ref = group.bvr_reference or group.compute_partner_bvr_ref()
            group.format_ref = slip_obj._space(ref.lstrip("0"))

    @api.multi
    def get_months(self, months, sponsorships):
        """
        Given the list of months to print,
        returns the list of months grouped by the frequency payment
        of the contract group and only containing unpaid sponsorships.
        :param months: list of dates (date, datetime or string)
        :param sponsorships: recordset of included sponsorships
        :return: list of dates grouped in string format
        """
        self.ensure_one()
        freq = self.advance_billing_months
        payment_mode = self.with_context(lang="en_US").payment_mode_id
        # Take first open invoice or next_invoice_date
        open_invoice = min([i for i in sponsorships.mapped("first_open_invoice") if i])
        if open_invoice:
            first_invoice_date = open_invoice.replace(day=1)
        else:
            raise odooWarning(_("No open invoice found !"))

        for i, month in enumerate(months):
            if isinstance(month, str):
                months[i] = fields.Date.from_string(month)
            if isinstance(month, datetime):
                months[i] = month.date()

        # check if first invoice is after last month
        if first_invoice_date > months[-1]:
            raise odooWarning(_(f"First invoice is after Date Stop"))

        # Only keep unpaid months
        valid_months = [
            fields.Date.to_string(month) for month in months
            if month >= first_invoice_date
        ]
        if "Permanent" in payment_mode.name:
            return valid_months[:1]
        if freq == 1:
            return valid_months
        else:
            # Group months
            result = list()
            count = 1
            month_start = ""
            for month in valid_months:
                if not month_start:
                    month_start = month
                if count < freq:
                    count += 1
                else:
                    result.append(month_start + " - " + month)
                    month_start = ""
                    count = 1
            if not result:
                result.append(month_start + " - " + month)
            return result

    @api.multi
    def get_communication(self, start, stop, sponsorships):
        """
        Get the communication to print on the payment slip for sponsorship
        :param start: the month start for which we print the payment slip (string)
        :param stop: the month stop for which we print the payment slip (string)
        :param sponsorships: recordset of sponsorships for which to print the
                             payment slips
        :return: string of the communication
        """
        self.ensure_one()
        payment_mode = self.with_context(lang="en_US").payment_mode_id
        amount = self._get_amount(start, stop, sponsorships)
        valid = sponsorships
        number_sponsorship = len(sponsorships)
        date_start = fields.Date.to_date(start)
        date_stop = fields.Date.to_date(stop)
        vals = {
            "amount": f"CHF {amount:.0f}",
            "subject": _("for") + " ",
            "date": "",
        }
        locale = self.partner_id.lang
        context = {"lang": locale}
        if start and stop:
            start_date = format_date(date_start, format="MMMM yyyy", locale=locale)
            stop_date = format_date(date_stop, format="MMMM yyyy", locale=locale)
            if start == stop:
                vals["date"] = start_date
            else:
                vals["date"] = f"{start_date} - {stop_date}"
        if "Permanent" in payment_mode.name:
            vals["payment_type"] = _("ISR for standing order")
            vals["date"] = ""
        else:
            vals["payment_type"] = (
                _("ISR") + " " + self.contract_ids[0].with_context(
                    context).group_freq
            )
        if number_sponsorship > 1:
            vals["subject"] += str(number_sponsorship) + " " + _("sponsorships")
        elif number_sponsorship and valid.child_id:
            vals["subject"] = valid.child_id.preferred_name + " ({})".format(
                valid.child_id.local_id
            )
        elif number_sponsorship and not valid.child_id and valid.display_name:
            product_name = self.env["product.product"].search(
                [("id", "in", valid.mapped("contract_line_ids.product_id").ids)]
            )

            vals["subject"] = ", ".join(product_name.mapped("thanks_name"))

        return (
            f"{vals['payment_type']} {vals['amount']}"
            f"<br/>{vals['subject']}<br/>{vals['date']}"
        )

    @api.model
    def get_scan_line(self, account, reference, amount=False):
        """ Generate a scan line given the reference """
        if amount:
            line = "01"
            decimal_amount, int_amount = math.modf(amount)
            str_amount = (
                str(int(int_amount)) + str(int(decimal_amount * 100)).rjust(2, "0")
            ).rjust(10, "0")
            line += str_amount
            line = mod10r(line)
        else:
            line = "042"
        line += ">"
        line += reference.replace(" ", "").rjust(27, "0")
        line += "+ "
        account_components = account.split("-")
        bank_identifier = (
            f"{account_components[0]}"
            f"{account_components[1].rjust(6, '0')}"
            f"{account_components[2]}"
        )
        line += bank_identifier
        line += ">"
        return line

    @api.model
    def get_company_bvr_account(self):
        """ Utility to find the bvr account of the company. """
        return COMPASSION_BVR

    def _get_amount(self, start, stop, sponsorships):
        amount = sum(sponsorships.mapped("total_amount"))
        months = int(stop.split("-")[1]) - int(start.split("-")[1]) + 1
        return amount * months
