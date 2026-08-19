"""seed diagnosis_codes with ICD-10 codes from codes.txt

Revision ID: 202608190002
Revises: 202608190001
Create Date: 2026-08-19 00:02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "202608190002"
down_revision: Union[str, None] = "202608190001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

diagnosis_codes_table = sa.table(
    "diagnosis_codes",
    sa.column("code", sa.String),
    sa.column("description", sa.Text),
)

DIAGNOSIS_CODES = [
    ("A00", "Cholera"),
    ("A01", "Typhoid and paratyphoid fevers"),
    ("A02", "Other salmonella infections"),
    ("A03", "Shigellosis"),
    ("A04", "Other bacterial intestinal infections"),
    ("A05", "Other bacterial foodborne intoxications, not elsewhere classified"),
    ("A06", "Amebiasis"),
    ("A07", "Other protozoal intestinal diseases"),
    ("A08", "Viral and other specified intestinal infections"),
    ("A09", "Infectious gastroenteritis and colitis, unspecified"),
    ("A15", "Respiratory tuberculosis"),
    ("A17", "Tuberculosis of nervous system"),
    ("A18", "Tuberculosis of other organs"),
    ("A19", "Miliary tuberculosis"),
    ("A20", "Plague"),
    ("A21", "Tularemia"),
    ("A22", "Anthrax"),
    ("A23", "Brucellosis"),
    ("A24", "Glanders and melioidosis"),
    ("A25", "Rat-bite fevers"),
    ("A26", "Erysipeloid"),
    ("A27", "Leptospirosis"),
    ("A28", "Other zoonotic bacterial diseases, not elsewhere classified"),
    ("A30", "Leprosy [Hansen's disease]"),
    ("A31", "Infection due to other mycobacteria"),
    ("A32", "Listeriosis"),
    ("A33", "Tetanus neonatorum"),
    ("A34", "Obstetrical tetanus"),
    ("A35", "Other tetanus"),
    ("A36", "Diphtheria"),
    ("A37", "Whooping cough"),
    ("A38", "Scarlet fever"),
    ("A39", "Meningococcal infection"),
    ("A40", "Streptococcal sepsis"),
    ("A41", "Other sepsis"),
    ("A42", "Actinomycosis"),
    ("A43", "Nocardiosis"),
    ("A44", "Bartonellosis"),
    ("A46", "Erysipelas"),
    ("A48", "Other bacterial diseases, not elsewhere classified"),
    ("A49", "Bacterial infection of unspecified site"),
    ("A50", "Congenital syphilis"),
    ("A51", "Early syphilis"),
    ("A52", "Late syphilis"),
    ("A53", "Other and unspecified syphilis"),
    ("A54", "Gonococcal infection"),
    ("A55", "Chlamydial lymphogranuloma (venereum)"),
    ("A56", "Other sexually transmitted chlamydial diseases"),
    ("A57", "Chancroid"),
    ("A58", "Granuloma inguinale"),
    ("A59", "Trichomoniasis"),
    ("A60", "Anogenital herpesviral [herpes simplex] infections"),
    ("A63", "Other predominantly sexually transmitted diseases, not elsewhere classified"),
    ("A64", "Unspecified sexually transmitted disease"),
    ("A65", "Nonvenereal syphilis"),
    ("A66", "Yaws"),
    ("A67", "Pinta [carate]"),
    ("A68", "Relapsing fevers"),
    ("A69", "Other spirochetal infections"),
    ("A70", "Chlamydia psittaci infections"),
    ("A71", "Trachoma"),
    ("A74", "Other diseases caused by chlamydiae"),
    ("A75", "Typhus fever"),
    ("A77", "Spotted fever [tick-borne rickettsioses]"),
    ("A78", "Q fever"),
    ("A79", "Other rickettsioses"),
    ("A80", "Acute poliomyelitis"),
    ("A81", "Atypical virus infections of central nervous system"),
    ("A82", "Rabies"),
    ("A83", "Mosquito-borne viral encephalitis"),
    ("A84", "Tick-borne viral encephalitis"),
    ("A85", "Other viral encephalitis, not elsewhere classified"),
    ("A86", "Unspecified viral encephalitis"),
    ("A87", "Viral meningitis"),
    ("A88", "Other viral infections of central nervous system, not elsewhere classified"),
    ("A89", "Unspecified viral infection of central nervous system"),
    ("A90", "Dengue fever [classical dengue]"),
    ("A91", "Dengue hemorrhagic fever"),
    ("A92", "Other mosquito-borne viral fevers"),
    ("A93", "Other arthropod-borne viral fevers, not elsewhere classified"),
    ("A94", "Unspecified arthropod-borne viral fever"),
    ("A95", "Yellow fever"),
    ("A96", "Arenaviral hemorrhagic fever"),
    ("A98", "Other viral hemorrhagic fevers, not elsewhere classified"),
    ("A99", "Unspecified viral hemorrhagic fever"),
    ("B00", "Herpesviral [herpes simplex] infections"),
    ("B01", "Varicella [chickenpox]"),
    ("B02", "Zoster [herpes zoster]"),
    ("B03", "Smallpox"),
    ("B04", "Monkeypox"),
    ("B05", "Measles"),
    ("B06", "Rubella [German measles]"),
    ("B07", "Viral warts"),
    ("B08", "Other viral infections characterized by skin and mucous membrane lesions, not elsewhere classified"),
    ("B09", "Unspecified viral infection characterized by skin and mucous membrane lesions"),
    ("B10", "Other human herpesviruses"),
    ("B15", "Acute hepatitis A"),
    ("B16", "Acute hepatitis B"),
    ("B17", "Other acute viral hepatitis"),
    ("B18", "Chronic viral hepatitis"),
]


def upgrade() -> None:
    op.bulk_insert(diagnosis_codes_table, [
        {"code": code, "description": description} for code, description in DIAGNOSIS_CODES
    ])


def downgrade() -> None:
    codes = [code for code, _ in DIAGNOSIS_CODES]
    op.execute(
        diagnosis_codes_table.delete().where(diagnosis_codes_table.c.code.in_(codes))
    )
