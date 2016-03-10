#include "LinkedList.h"

template <class T>
LinkedList<T>::LinkedList()
{
  this->succ = 0;
  this->prev = 0;
  
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
    LinkedList<T>* newel = new LinkedList<T>();
    this->prev = newel;
    
  }
}

template <class T>
T LinkedList<T>::remove()
{
  T value = this->value;
  //TODO delete this element
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

