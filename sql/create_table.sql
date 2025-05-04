CREATE TABLE skillfactory_grader (
    id SERIAL NOT NULL PRIMARY KEY,
    user_id TEXT NOT NULL,
    client_token TEXT NOT NULL,
    result_source TEXT,
    outcome_service TEXT,
    is_correct INT,
    attempt_type TEXT,
    created_at TIMESTAMPTZ(6)
)