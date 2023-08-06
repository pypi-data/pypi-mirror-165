from hackle.decision import ExperimentDecision, FeatureFlagDecision, DecisionReason
from hackle.entities import EventType
from hackle.event.user_event import UserEvent


class InternalClient(object):

    def __init__(self, evaluator, workspace_fetcher, event_processor, logger):
        self.evaluator = evaluator
        self.workspace_fetcher = workspace_fetcher
        self.event_processor = event_processor
        self.logger = logger

    def close(self):
        self.workspace_fetcher.stop()
        self.event_processor.stop()

    def experiment(self, experiment_key, user, default_variation_key):
        workspace = self.workspace_fetcher.get_workspace()
        if workspace is None:
            return ExperimentDecision(default_variation_key, DecisionReason.SDK_NOK_READY)

        experiment = workspace.get_experiment_or_none(experiment_key)
        if experiment is None:
            return ExperimentDecision(default_variation_key, DecisionReason.EXPERIMENT_NOT_FOUND)

        evaluation = self.evaluator.evaluate(workspace, experiment, user, default_variation_key)
        self.event_processor.process(UserEvent.exposure(experiment, user, evaluation))

        return ExperimentDecision(evaluation.variation_key, evaluation.reason)

    def feature_flag(self, feature_key, user):
        workspace = self.workspace_fetcher.get_workspace()
        if workspace is None:
            return FeatureFlagDecision(False, DecisionReason.SDK_NOK_READY)

        feature_flag = workspace.get_feature_flag_or_none(feature_key)
        if feature_flag is None:
            return FeatureFlagDecision(False, DecisionReason.FEATURE_FLAG_NOT_FOUND)

        evaluation = self.evaluator.evaluate(workspace, feature_flag, user, 'A')
        self.event_processor.process(UserEvent.exposure(feature_flag, user, evaluation))

        if evaluation.variation_key == 'A':
            return FeatureFlagDecision(False, evaluation.reason)
        else:
            return FeatureFlagDecision(True, evaluation.reason)

    def track_event(self, event, user):
        event_type = self._event_type(event)
        self.event_processor.process(UserEvent.track(event_type, event, user))
        return

    def _event_type(self, event):
        config = self.workspace_fetcher.get_workspace()

        if not config:
            return EventType(0, event.key)

        event_type = config.get_event_type_or_none(event.key)

        if not event_type:
            return EventType(0, event.key)

        return event_type
