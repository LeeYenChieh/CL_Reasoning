from Strategy.RepairOnlyOneLanguage import RepairOnlyOneLanguage
from Log.Log import Log
from File.File import File


class RepairEnglishVariant(RepairOnlyOneLanguage):
    """
    Repair pass for the Experiment 2-4 evaluation output (rewritten-English + prompt style).

    Identical to RepairOnlyOneLanguage in every respect except that the StrategyConfig is
    reconstructed from the result file's own metadata instead of being supplied by the
    caller. This is what carries `languages` and `promptStyle` back into the re-run, so a
    repaired record is regenerated with the exact same prompt as the original pass.
    The Dataset is still rebuilt from `file.getDatasetConfig()` by the parent, so its
    `useRewrite` / `language` flags are preserved automatically.
    """
    def __init__(self, log: Log, file: File):
        super().__init__(file.getStrategyConfig(), log, file)
