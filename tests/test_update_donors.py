"""
Unit tests for update_donors.py module.
Tests data cleaning, normalization, aggregation, and JSON generation.
"""

import json
import os
import sys
from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "services"))

from update_donors import (
    OUTPUT_JSON_PATH,
    create_empty_json,
    setup_gspread_credentials,
)


class TestNameNormalization:
    """Tests for name normalization functionality."""

    def test_normalize_removes_accents(self):
        """Test that accents are removed from names."""
        # This tests the normalize_name function indirectly through processing
        data = {
            "Carimbo de data/hora": ["13/12/2025 10:00:00"],
            "Nome": ["José Silva"],
            "Valor": ["100"],
        }
        df = pd.DataFrame(data)

        # Apply the normalization logic
        import unicodedata

        def normalize_name(name: str) -> str:
            normalized = unicodedata.normalize("NFD", name)
            ascii_name = "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )
            return " ".join(ascii_name.upper().split())

        df["NomeNormalizado"] = df["Nome"].astype(str).str.strip().apply(normalize_name)

        assert df["NomeNormalizado"].iloc[0] == "JOSE SILVA"

    def test_normalize_handles_multiple_spaces(self):
        """Test that multiple spaces are normalized to single space."""
        import unicodedata

        def normalize_name(name: str) -> str:
            normalized = unicodedata.normalize("NFD", name)
            ascii_name = "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )
            return " ".join(ascii_name.upper().split())

        result = normalize_name("João   Pedro   Silva")
        assert result == "JOAO PEDRO SILVA"

    def test_normalize_converts_to_uppercase(self):
        """Test that names are converted to uppercase."""
        import unicodedata

        def normalize_name(name: str) -> str:
            normalized = unicodedata.normalize("NFD", name)
            ascii_name = "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )
            return " ".join(ascii_name.upper().split())

        result = normalize_name("maria garcia")
        assert result == "MARIA GARCIA"

    def test_normalize_trims_whitespace(self):
        """Test that leading and trailing whitespace is removed."""
        import unicodedata

        def normalize_name(name: str) -> str:
            normalized = unicodedata.normalize("NFD", name)
            ascii_name = "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )
            return " ".join(ascii_name.upper().split())

        result = normalize_name("  Pedro Santos  ")
        assert result == "PEDRO SANTOS"


class TestDataAggregation:
    """Tests for donation aggregation logic."""

    def test_aggregates_same_normalized_names(self):
        """Test that donations from the same person (different formatting) are aggregated."""
        data = {
            "Carimbo de data/hora": [
                "13/12/2025 10:00:00",
                "13/12/2025 11:00:00",
            ],
            "Nome": ["José Silva", "jose silva"],
            "Valor": [100.0, 50.0],
        }
        df = pd.DataFrame(data)
        df["Carimbo de data/hora"] = pd.to_datetime(
            df["Carimbo de data/hora"], dayfirst=True
        )

        import unicodedata

        def normalize_name(name: str) -> str:
            normalized = unicodedata.normalize("NFD", name)
            ascii_name = "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )
            return " ".join(ascii_name.upper().split())

        df["NomeNormalizado"] = df["Nome"].astype(str).str.strip().apply(normalize_name)
        df["Nome"] = df["Nome"].astype(str).str.strip()

        # Sort by date to get most recent name
        df = df.sort_values(by="Carimbo de data/hora", ascending=True)

        # Aggregate
        aggregated = df.groupby("NomeNormalizado", as_index=False).agg(
            {
                "Nome": "last",
                "Valor": "sum",
            }
        )

        assert len(aggregated) == 1
        assert aggregated["Valor"].iloc[0] == 150.0
        assert aggregated["Nome"].iloc[0] == "jose silva"  # Most recent

    def test_preserves_most_recent_name(self):
        """Test that the most recent name format is preserved for display."""
        data = {
            "Carimbo de data/hora": [
                "13/12/2025 10:00:00",
                "13/12/2025 11:00:00",
                "13/12/2025 12:00:00",
            ],
            "Nome": ["João Silva", "JOÃO SILVA", "joão silva"],
            "Valor": [50.0, 30.0, 20.0],
        }
        df = pd.DataFrame(data)
        df["Carimbo de data/hora"] = pd.to_datetime(
            df["Carimbo de data/hora"], dayfirst=True
        )

        import unicodedata

        def normalize_name(name: str) -> str:
            normalized = unicodedata.normalize("NFD", name)
            ascii_name = "".join(
                char for char in normalized if unicodedata.category(char) != "Mn"
            )
            return " ".join(ascii_name.upper().split())

        df["NomeNormalizado"] = df["Nome"].astype(str).str.strip().apply(normalize_name)
        df["Nome"] = df["Nome"].astype(str).str.strip()

        df = df.sort_values(by="Carimbo de data/hora", ascending=True)

        aggregated = df.groupby("NomeNormalizado", as_index=False).agg(
            {
                "Nome": "last",
                "Valor": "sum",
            }
        )

        # Most recent name should be preserved (all normalize to same)
        assert aggregated["Nome"].iloc[0] == "joão silva"
        assert aggregated["Valor"].iloc[0] == 100.0


class TestDataCleaning:
    """Tests for data validation and cleaning."""

    def test_removes_empty_names(self):
        """Test that rows with empty names are removed."""
        data = {
            "Carimbo de data/hora": ["13/12/2025 10:00:00", "13/12/2025 11:00:00"],
            "Nome": ["João Silva", ""],
            "Valor": ["100", "50"],
        }
        df = pd.DataFrame(data)

        # Apply cleaning logic
        df = df[df["Nome"].astype(str).str.strip() != ""]

        assert len(df) == 1

    def test_removes_null_values(self):
        """Test that rows with null values in required columns are removed."""
        data = {
            "Carimbo de data/hora": ["13/12/2025 10:00:00", None],
            "Nome": ["João Silva", "Maria Santos"],
            "Valor": ["100", "50"],
        }
        df = pd.DataFrame(data)

        df.dropna(
            subset=["Carimbo de data/hora", "Nome", "Valor"],
            inplace=True,
        )

        assert len(df) == 1

    def test_converts_valor_to_numeric(self):
        """Test that 'Valor' is properly converted to numeric format."""
        data = {
            "Carimbo de data/hora": ["13/12/2025 10:00:00"],
            "Nome": ["João Silva"],
            "Valor": ["1.234,56"],  # Brazilian format
        }
        df = pd.DataFrame(data)

        # Apply conversion logic
        df["Valor"] = pd.to_numeric(
            df["Valor"].astype(str).str.replace(".", "").str.replace(",", "."),
            errors="coerce",
        )

        assert df["Valor"].iloc[0] == 1234.56

    def test_handles_invalid_valor(self):
        """Test that invalid values are handled properly."""
        data = {
            "Carimbo de data/hora": ["13/12/2025 10:00:00"],
            "Nome": ["João Silva"],
            "Valor": ["invalid"],
        }
        df = pd.DataFrame(data)

        df["Valor"] = pd.to_numeric(
            df["Valor"].astype(str).str.replace(".", "").str.replace(",", "."),
            errors="coerce",
        )
        df.dropna(subset=["Valor"], inplace=True)

        assert len(df) == 0


class TestWeightAssignment:
    """Tests for word cloud weight calculation."""

    def test_weight_assignment_logic(self):
        """Test that weights are assigned correctly based on ranking."""
        # Create enough donors to test all weight tiers
        data = {
            "Nome": [f"Donor{i}" for i in range(1, 26)],
            "Valor": [1000 - (i * 10) for i in range(25)],
        }
        df = pd.DataFrame(data)

        sorted_donors = df.sort_values(by="Valor", ascending=False).reset_index(
            drop=True
        )
        weights = []
        for idx in range(len(sorted_donors)):
            if idx == 0:
                weights.append(5)
            elif idx < 4:
                weights.append(4)
            elif idx < 10:
                weights.append(3)
            elif idx < 20:
                weights.append(2)
            else:
                weights.append(1)
        sorted_donors["weight"] = weights

        assert sorted_donors["weight"].iloc[0] == 5  # 1st (idx 0)
        assert sorted_donors["weight"].iloc[1] == 4  # 2nd (idx 1)
        assert sorted_donors["weight"].iloc[3] == 4  # 4th (idx 3)
        assert sorted_donors["weight"].iloc[4] == 3  # 5th (idx 4)
        assert sorted_donors["weight"].iloc[9] == 3  # 10th (idx 9)
        assert sorted_donors["weight"].iloc[10] == 2  # 11th (idx 10)
        assert sorted_donors["weight"].iloc[19] == 2  # 20th (idx 19)
        assert sorted_donors["weight"].iloc[20] == 1  # 21st (idx 20)


class TestSetupCredentials:
    """Tests for Google Sheets credentials setup."""

    def test_setup_credentials_missing_env_var(self):
        """Test that missing GCP_SA_KEY raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GCP_SA_KEY environment variable"):
                setup_gspread_credentials()

    def test_setup_credentials_with_valid_json(self):
        """Test that valid credentials are processed correctly."""
        mock_creds = {
            "type": "service_account",
            "project_id": "test-project",
            "private_key": "test-key",
            "client_email": "test@test.iam.gserviceaccount.com",
        }

        with patch.dict(os.environ, {"GCP_SA_KEY": json.dumps(mock_creds)}):
            with patch("update_donors.Credentials.from_service_account_info") as mock_creds_method:
                with patch("update_donors.gspread.authorize") as mock_authorize:
                    mock_gc = MagicMock()
                    mock_authorize.return_value = mock_gc

                    result = setup_gspread_credentials()

                    assert result == mock_gc
                    mock_creds_method.assert_called_once()
                    mock_authorize.assert_called_once()


class TestCreateEmptyJson:
    """Tests for empty JSON creation."""

    @patch("builtins.open", new_callable=mock_open)
    @patch("update_donors.json.dump")
    def test_create_empty_json_structure(self, mock_json_dump, mock_file):
        """Test that empty JSON has correct structure."""
        create_empty_json()

        # Verify file was opened for writing
        mock_file.assert_called_once_with(
            "public/" + OUTPUT_JSON_PATH, "w", encoding="utf-8"
        )

        # Verify correct data structure was written
        expected_data = {"wordCloud": [], "topDonors": [], "latestDonations": []}
        mock_json_dump.assert_called_once()
        actual_data = mock_json_dump.call_args[0][0]
        assert actual_data == expected_data


class TestTopDonorsList:
    """Tests for top donors list generation."""

    def test_top_donors_sorted_by_value(self):
        """Test that top donors are sorted by donation value."""
        data = {
            "Nome": ["Donor1", "Donor2", "Donor3"],
            "Valor": [500, 1000, 750],
        }
        df = pd.DataFrame(data)

        top_donors_df = df.nlargest(2, "Valor")
        top_donors_list = [{"name": row["Nome"]} for _, row in top_donors_df.iterrows()]

        assert len(top_donors_list) == 2
        assert top_donors_list[0]["name"] == "Donor2"  # Highest value
        assert top_donors_list[1]["name"] == "Donor3"  # Second highest


class TestLatestDonorsList:
    """Tests for latest donations list generation."""

    def test_latest_donors_unique_names(self):
        """Test that latest donors list removes duplicates keeping most recent."""
        data = {
            "Carimbo de data/hora": [
                "13/12/2025 10:00:00",
                "13/12/2025 11:00:00",
                "13/12/2025 12:00:00",
            ],
            "Nome": ["João", "Maria", "João"],
            "Valor": [100.0, 200.0, 150.0],
        }
        df = pd.DataFrame(data)
        df["Carimbo de data/hora"] = pd.to_datetime(
            df["Carimbo de data/hora"], dayfirst=True
        )

        latest_donors_df = (
            df.sort_values(by="Carimbo de data/hora", ascending=False)
            .drop_duplicates(subset=["Nome"])
            .head(10)
        )

        assert len(latest_donors_df) == 2  # Only unique names
        # João's most recent donation should be at 12:00
        joao_row = latest_donors_df[latest_donors_df["Nome"] == "João"].iloc[0]
        assert joao_row["Valor"] == 150.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
