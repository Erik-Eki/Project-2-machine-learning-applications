{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (<ipython-input-1-4bb90dce6fd8>, line 1)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-1-4bb90dce6fd8>\"\u001b[0;36m, line \u001b[0;32m1\u001b[0m\n\u001b[0;31m    def nopeudet(df)\u001b[0m\n\u001b[0m                    ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "def nopeudet(df):\n",
    "    \n",
    "\n",
    "    df['distancex'] = df['x'].diff()\n",
    "df['distancey'] = df['y'].diff()\n",
    "df['distance'] = (df['distancex']**2 + df['distancey']**2)\n",
    "df['distance'] = (np.sqrt(df['distance'])/161.15)\n",
    "\n",
    "df = df.drop('distancex', 1)\n",
    "df = df.drop('distancey', 1)\n",
    "\n",
    "\n",
    "#df['distance'] = ((np.sqrt((df['x'] - df['x'].shift(-1))**2 + (df['y'] - df['y'].shift(-1))**2))/161.15)\n",
    "#df['distance'] = ((np.sqrt((df['x'].diff()**2 + (df['y'].diff()**2))/161.15)))\n",
    "\n",
    "\n",
    "df['ero'] = df['timestamp'].diff()\n",
    "df['ero'] = df.ero.dt.seconds                   \n",
    "                   \n",
    "df['speedkm'] = df['distance']/df['ero']*3.6\n",
    "\n",
    "\n",
    "    # Poistetaan liian nopeat, yli 7km/h\n",
    "#df = df.drop(df[(df.speedkm > 7)].index)\n",
    "    \n",
    "df = df.dropna()\n",
    "df\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
