from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from requests_app.models import Category, ServiceRequest

User = get_user_model()
requester, _ = User.objects.get_or_create(username="requester1")
electrical, _ = Category.objects.get_or_create(
    name="Electrical", defaults={"description": "Electrical faults and maintenance"}
)
ict, _ = Category.objects.get_or_create(
    name="ICT Support", defaults={"description": "Computers, networks and software"}
)

# Start clean so the script can be re-run
ServiceRequest.objects.filter(title__startswith="Lab3 ").delete()

now = timezone.now()

print("=== TASK 1: requests with different due dates ===")
ServiceRequest.objects.create(
    requester=requester, category=ict, title="Lab3 due soon",
    description="Synthetic laboratory record.", location="Lab 2",
    priority=3, due_at=now + timedelta(hours=2),
)
ServiceRequest.objects.create(
    requester=requester, category=ict, title="Lab3 due later",
    description="Synthetic laboratory record.", location="Lab 2",
    priority=3, due_at=now + timedelta(days=3),
)
chosen = now + timedelta(days=1)
print("Chosen time:", chosen)
print(list(
    ServiceRequest.objects.filter(due_at__lt=chosen, title__startswith="Lab3 ")
    .values_list("title", "due_at")
))

print()
print("=== TASK 3: ten synthetic requests ===")
specs = [
    (electrical, "open", 1), (electrical, "open", 3),
    (electrical, "assigned", 2), (electrical, "assigned", 5),
    (electrical, "resolved", 4),
    (ict, "open", 2), (ict, "assigned", 1), (ict, "resolved", 3),
    (ict, "open", 4), (ict, "resolved", 5),
]
for i, (cat, status, prio) in enumerate(specs, 1):
    data = dict(
        requester=requester, category=cat, title=f"Lab3 synthetic {i}",
        description="Synthetic laboratory record.", location="Lab 2",
        priority=prio, status=status,
    )
    if status == "resolved":
        data["resolved_at"] = now
        data["resolution_summary"] = "Synthetic resolution."
    ServiceRequest.objects.create(**data)

print("Total Lab3 requests:", ServiceRequest.objects.filter(title__startswith="Lab3 ").count())

qs = ServiceRequest.objects.filter(
    category=electrical, status__in=["open", "assigned"]
).order_by("priority", "created_at")

print()
print("--- queryset.query ---")
print(qs.query)
print()
print("--- queryset.explain() ---")
print(qs.explain())
print()
print("--- results ---")
for r in qs:
    print(r.priority, r.status, r.title)