package persistence

import (
	"context"
	"time"
)

type observationKey struct{}
type observation func(string, time.Duration, bool)

// WithObservation attaches a request-scoped timing sink. It receives only
// fixed stage names, durations and failure flags, never SQL or player data.
func WithObservation(ctx context.Context, sink func(string, time.Duration, bool)) context.Context {
	return context.WithValue(ctx, observationKey{}, observation(sink))
}

func observeStage(ctx context.Context, stage string) func(error) {
	sink, _ := ctx.Value(observationKey{}).(observation)
	if sink == nil {
		return func(error) {}
	}
	started := time.Now()
	return func(err error) { sink(stage, time.Since(started), err != nil) }
}
