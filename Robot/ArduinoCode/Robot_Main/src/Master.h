#ifndef Master_h
#define Master_h

class Master
{
public:
    enum State
    {
        Initializing,
        Offline,
        Player,
        Auto
    };
    Master();
    ~Master();

    void ChangeState(State state);

private:
    State _requestedState = Initializing;
    State _state = Initializing;
};

#endif