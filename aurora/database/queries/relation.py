from sqlalchemy.orm import Session

from aurora.database import models


def relate_samples(
    db: Session, this: models.Sample, related: models.Sample, **kwargs
) -> None:

    this.add_child_sample(related)
    db.commit()
