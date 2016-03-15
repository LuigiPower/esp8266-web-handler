#include "LinkedList.h"

template <class T>
LinkedList<T>::LinkedList()
{
    this->succ = 0;
    this->prev = 0;
}

template <class T>
LinkedList<T>::LinkedList(T val)
{
  this->succ = this;
  this->prev = this;
  this->value = val;
}

template <class T>
LinkedList<T>::~LinkedList()
{

}

template <class T>
void LinkedList<T>::insert(T val)
{
    if(this->succ == 0 && this->prev == 0)
    {
        this->succ = this;
        this->prev = this;
        this->value = val;
    }
    else
    {
        LinkedList<T>* newel = new LinkedList<T>(val);
        LinkedList<T>* nextel = this->succ;
        this->succ = newel;
        nextel->prev = newel;
        newel->prev = this;
        newel->succ = nextel;
    }
}

template <class T>
T LinkedList<T>::remove()
{
    if(this->succ == this->prev)
    {
        T value = this->value;

        this->succ = 0;
        this->prev = 0;
    }
    else
    {
        T value = this->value;

        this->prev->succ = this->succ;
        this->succ->prev = this->prev;
    }

    delete this;
    return value;
}

template <class T>
LinkedList<T>* LinkedList<T>::next()
{
    return succ;
}


template <class T>
T LinkedList<T>::set(T newvalue)
{
    T oldvalue;
    this->value = newvalue;
    return oldvalue;
}

