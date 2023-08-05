import pytest

from tests.models.helpers import do_test_fix_max_steps


@pytest.mark.parametrize("max_epochs", (1, 2))
@pytest.mark.parametrize("accumulate_grad_batches", (1, 3))
@pytest.mark.parametrize("batch_size" , (1, 2, 3, 8, 11))
def test_fix_max_steps_cpu(max_epochs, accumulate_grad_batches, batch_size):

    do_test_fix_max_steps(
        max_epochs,
        accumulate_grad_batches,
        batch_size,
        accelerator="cpu",
    )

    do_test_fix_max_steps(
        max_epochs,
        accumulate_grad_batches,
        batch_size,
        accelerator="cpu",
        strategy="ddp",
        devices=10,
    )
