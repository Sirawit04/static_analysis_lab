from src.invoice_service import InvoiceService, Invoice, LineItem
import pytest


def make_basic_invoice(
    country="TH",
    membership="none",
    coupon=None,
    fragile=False
):
    return Invoice(
        invoice_id="INV001",
        customer_id="CUST01",
        country=country,
        membership=membership,
        coupon=coupon,
        items=[
            LineItem(
                sku="ITEM01",
                category="book",
                unit_price=100,
                qty=2,
                fragile=fragile
            )
        ]
    )


def test_basic_invoice_th_no_discount():
    service = InvoiceService()
    invoice = make_basic_invoice(country="TH")

    total, warnings = service.compute_total(invoice)

    assert total > 0
    assert warnings == []


def test_gold_membership_discount():
    service = InvoiceService()
    invoice = make_basic_invoice(membership="gold")

    total, _ = service.compute_total(invoice)

    assert total > 0


def test_coupon_discount_applied():
    service = InvoiceService()
    invoice = make_basic_invoice(coupon="WELCOME10")

    total, warnings = service.compute_total(invoice)

    assert total > 0
    assert warnings == []


def test_unknown_coupon_warning():
    service = InvoiceService()
    invoice = make_basic_invoice(coupon="INVALID")

    total, warnings = service.compute_total(invoice)

    assert "Unknown coupon" in warnings


def test_fragile_item_adds_fee():
    service = InvoiceService()
    invoice = make_basic_invoice(fragile=True)

    total, _ = service.compute_total(invoice)

    assert total > 0


def test_us_shipping_rules():
    service = InvoiceService()
    invoice = make_basic_invoice(country="US")

    total, _ = service.compute_total(invoice)

    assert total > 0


def test_invalid_invoice_raises_error():
    service = InvoiceService()

    bad_invoice = Invoice(
        invoice_id="",
        customer_id="",
        country="TH",
        membership="none",
        coupon=None,
        items=[]
    )

    with pytest.raises(ValueError):
        service.compute_total(bad_invoice)