"""
pet_health_engine.py

Responsibilities:
- Convert work context into pet health
- Calculate hunger
- Calculate energy
- Calculate confidence
- Calculate mood
- Determine overall status

This module contains deterministic business rules.

No AI should be used here.
"""


class PetHealthEngine:
    def calculate_pet_health(self, context: dict) -> dict:
        """
        Calculate Byte's health based on work context.

        Parameters:
            context (dict)

        Returns:
            dict
        """

        hunger = self._calculate_hunger(context)
        energy = self._calculate_energy(context)
        confidence = self._calculate_confidence(context)

        mood = self._determine_mood(
            hunger,
            energy,
            confidence
        )

        status = self._determine_status(
            hunger,
            energy,
            confidence
        )

        return {
            "hunger": hunger,
            "energy": energy,
            "confidence": confidence,
            "mood": mood,
            "status": status
        }

    def _calculate_hunger(self, context: dict) -> int:
        """
        Hunger represents neglected responsibilities.
        Higher = Worse.
        """

        hunger = 0

        hunger += context["unread_messages"] * 5
        hunger += context["unanswered_emails"] * 10
        hunger += context["pending_manager_requests"] * 15
        hunger += context["overdue_tasks"] * 20

        return min(hunger, 100)

    def _calculate_energy(self, context: dict) -> int:
        """
        Energy represents workload strain.
        Higher = Better.
        """

        energy = 100

        meetings = context["meetings_today"]

        energy -= meetings * 5

        return max(energy, 0)

    def _calculate_confidence(self, context: dict) -> int:
        """
        Confidence represents control of responsibilities.
        Higher = Better.
        """

        confidence = 100

        confidence -= context["overdue_tasks"] * 15
        confidence -= context["pending_manager_requests"] * 10

        if not context["timesheet_submitted"]:
            confidence -= 25

        return max(confidence, 0)

    def _determine_mood(
        self,
        hunger: int,
        energy: int,
        confidence: int
    ) -> str:
        """
        Determine Byte's emotional state.
        """

        overall_score = (
            (100 - hunger)
            + energy
            + confidence
        ) / 3

        if overall_score >= 80:
            return "happy"

        if overall_score >= 60:
            return "content"

        if overall_score >= 40:
            return "worried"

        return "sad"

    def _determine_status(
        self,
        hunger: int,
        energy: int,
        confidence: int
    ) -> str:
        """
        Determine overall health status.
        """

        if hunger >= 75:
            return "hungry"

        if energy <= 30:
            return "tired"

        if confidence <= 40:
            return "stressed"

        return "healthy"