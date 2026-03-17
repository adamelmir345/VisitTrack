import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import os

# ──────────────────────────────────────────
# CLASSE : GenerateurQR
# ──────────────────────────────────────────
class GenerateurQR:
    def __init__(self, dossier="billets_qr"):
        self.dossier = dossier
        os.makedirs(dossier, exist_ok=True)  # crée le dossier si il n'existe pas

    def generer(self, code, nom_fichier=None):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(code)
        qr.make(fit=True)

        image = qr.make_image(fill_color="black", back_color="white")

        if nom_fichier is None:
            nom_fichier = f"{code[:8]}.png"

        chemin = os.path.join(self.dossier, nom_fichier)
        image.save(chemin)
        print(f"QR Code genere : {chemin}")
        return chemin


# ──────────────────────────────────────────
# CLASSE : GenerateurPDF
# ──────────────────────────────────────────
class GenerateurPDF:
    def __init__(self, dossier="billets_pdf"):
        self.dossier = dossier
        os.makedirs(dossier, exist_ok=True)

    def creer_billet(self, reservation, chemin_qr):
        nom_fichier = f"billet_{reservation.id}.pdf"
        chemin_pdf = os.path.join(self.dossier, nom_fichier)

        doc = SimpleDocTemplate(chemin_pdf, pagesize=A4)
        styles = getSampleStyleSheet()
        contenu = []

        # ── Titre ──────────────────────────────
        style_titre = ParagraphStyle(
            "titre",
            parent=styles["Title"],
            fontSize=22,
            textColor=colors.HexColor("#1F3864"),
            spaceAfter=10,
        )
        contenu.append(Paragraph("VisitTrack – E-Billet", style_titre))
        contenu.append(Spacer(1, 0.3 * cm))

        # ── Ligne de séparation ────────────────
        contenu.append(Paragraph("─" * 60, styles["Normal"]))
        contenu.append(Spacer(1, 0.3 * cm))

        # ── Infos circuit ──────────────────────
        style_label = ParagraphStyle(
            "label",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#555555"),
        )
        style_valeur = ParagraphStyle(
            "valeur",
            parent=styles["Normal"],
            fontSize=13,
            textColor=colors.HexColor("#1F3864"),
            spaceAfter=6,
        )

        contenu.append(Paragraph("Circuit", style_label))
        contenu.append(Paragraph(reservation.circuit.titre, style_valeur))

        contenu.append(Paragraph("Destination", style_label))
        contenu.append(Paragraph(reservation.circuit.destination, style_valeur))

        contenu.append(Paragraph("Date de visite", style_label))
        contenu.append(Paragraph(str(reservation.date), style_valeur))

        contenu.append(Paragraph("Touriste", style_label))
        contenu.append(Paragraph(
            f"{reservation.touriste.prenom} {reservation.touriste.nom}",
            style_valeur
        ))

        contenu.append(Paragraph("Nombre de participants", style_label))
        contenu.append(Paragraph(str(reservation.nb_participants), style_valeur))

        contenu.append(Paragraph("Montant total", style_label))
        contenu.append(Paragraph(f"{reservation.montant_total} MAD", style_valeur))

        contenu.append(Paragraph("Statut", style_label))
        contenu.append(Paragraph(reservation.statut.upper(), style_valeur))

        contenu.append(Spacer(1, 0.5 * cm))
        contenu.append(Paragraph("─" * 60, styles["Normal"]))
        contenu.append(Spacer(1, 0.3 * cm))

        # ── QR Code ────────────────────────────
        contenu.append(Paragraph("Code de pointage :", style_label))
        contenu.append(Spacer(1, 0.2 * cm))
        contenu.append(Image(chemin_qr, width=5 * cm, height=5 * cm))
        contenu.append(Spacer(1, 0.2 * cm))
        contenu.append(Paragraph(
            f"Code : {reservation.billet.code_qr}",
            style_label
        ))

        contenu.append(Spacer(1, 0.5 * cm))
        contenu.append(Paragraph(
            "Presentez ce billet au guide le jour de votre visite.",
            styles["Italic"]
        ))

        doc.build(contenu)
        print(f"PDF genere : {chemin_pdf}")
        return chemin_pdf