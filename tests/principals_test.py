from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
import logging

# Configure the logger
logger = logging.getLogger(__name__)

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    assignment_id = 5
    # Ensure the assignment is in DRAFT state
    Assignment.set_status_by_id(assignment_id, AssignmentStateEnum.DRAFT)

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    
    assert response.status_code == 400
    response = response.json


def test_grade_assignment(client, h_principal):
    assignment_id = 4
    # Ensure the assignment is in SUBMITTED state
    Assignment.set_status_by_id(assignment_id, AssignmentStateEnum.SUBMITTED)

    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            'id': assignment_id,
            'grade': GradeEnum.C.value
        }
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    assignment_id = 4
    # Ensure the assignment is in GRADED state
    Assignment.set_status_by_id(assignment_id, AssignmentStateEnum.GRADED)

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
