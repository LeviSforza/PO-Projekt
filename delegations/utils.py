from delegations.models import Billing, Delegation, BusinessExpenses, UsersDelegations


# def createDelegationsCompanionObjects(delegation_id):
#     billing = Billing.objects.create(
#         FK_delegation=Delegation.objects.get(id_delegation=delegation_id))
#     BusinessExpenses.objects.create(FK_billing=Billing.objects.get(id_billing=billing.id_billing))


def getBusinessExpenses(delegation_id):
    billing = Billing.objects.get(
        FK_delegation=Delegation.objects.get(id_delegation=delegation_id))
    return BusinessExpenses.objects.get(FK_billing=billing)


def getParticipantsList(delegation_id):
    curr_delegation = Delegation.objects.get(pk=delegation_id)
    participants_list = [curr_delegation.FK_organizer]
    for inst in UsersDelegations.objects.all():
        if inst.FK_delegation.id_delegation == delegation_id:
            participants_list.append(inst.FK_user)
    return participants_list
