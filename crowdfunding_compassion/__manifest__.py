##############################################################################
#
#       ______ Releasing children from poverty      _
#      / ____/___  ____ ___  ____  ____ ___________(_)___  ____
#     / /   / __ \/ __ `__ \/ __ \/ __ `/ ___/ ___/ / __ \/ __ \
#    / /___/ /_/ / / / / / / /_/ / /_/ (__  |__  ) / /_/ / / / /
#    \____/\____/_/ /_/ /_/ .___/\__,_/____/____/_/\____/_/ /_/
#                        /_/
#                            in Jesus' name
#
#    Copyright (C) 2020 Compassion CH (http://www.compassion.ch)
#    @author: Quentin Gigon, Sylvain Losey, Emanuel Cino, Stephane Eicher
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# pylint: disable=C8101
{
    "name": "Crowdfunding Compassion",
    "version": "12.0.1.0.1",
    "author": "Compassion CH",
    "license": "AGPL-3",
    "website": "http://www.compassion.ch",
    "depends": [
        "cms_form_compassion",  # compassion-modules
        "theme_crowdfunding",  # compassion-switzerland
        "sponsorship_switzerland",  # compassion-switzerland
        "crm_compassion",  # compassion-modules
        "event",  # odoo base modules
    ],
    "data": [
        "data/crowdfunding_website.xml",
        "data/crowdfunding_event_type.xml",
        "data/email_templates.xml",
        "data/product.xml",
        "data/utm_medium.xml",
        "security/ir.model.access.csv",
        "views/account_invoice_line_view.xml",
        "views/crowdfunding_participant_view.xml",
        "views/crowdfunding_project_settings.xml",
        "views/crowdfunding_project_view.xml",
        "views/product_view.xml",
        "views/res_partner_view.xml",
        "views/assets.xml",
        "templates/crowdfunding_components.xml",
        "templates/crowdfunding_form_template.xml",
        "templates/homepage.xml",
        "templates/myaccount_components.xml",
        "templates/myaccount_crowdfunding_page.xml",
        "templates/project_creation_page.xml",
        "templates/project_donation_form_page.xml",
        "templates/project_donation_page.xml",
        "templates/project_page.xml",
        "templates/projects_list_page.xml",
    ],
    "demo": ["demo/demo.xml"],
    "installable": True,
    "auto_install": False,
}