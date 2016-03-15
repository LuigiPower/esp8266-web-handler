#ifndef __LINKED_LIST_H__
#define __LINKED_LIST_H__

template <class T>
class LinkedList
{
  private:
    LinkedList<T>* succ;
    LinkedList<T>* prev;
    T value;

  public:
    LinkedList();
    LinkedList(T val);
    ~LinkedList();

    /**
     * @return next LinkedList pointer
     */
    virtual LinkedList<T>* next();

    /**
     * Inserts new element after this one
     */
    virtual void insert(T value);

    /**
     * Removes current element from list
     */
    virtual T remove();

    /**
     * Sets current node value
     */
     virtual T set(T newvalue);
};

#endif
